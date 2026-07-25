import datetime
import http.server

import json
import random
import socket
import ssl
import socketserver
import sys
import threading
import time
from typing import cast
import requests
from requests.adapters import HTTPAdapter

ZEN_HOST = "opencode.ai"
ZEN_PATH = "/zen/v1"
TIMEOUT = 120
CLEANUP_INTERVAL = 300
MAX_IDLE = 3600
MAX_REQS_PER_CLIENT = 200
BAN_WINDOW = 600
FREE_LIMIT_ERR = "FreeUsageLimitError"


def next_utc_midnight():
    now = datetime.datetime.now(datetime.timezone.utc)
    tomorrow = now + datetime.timedelta(days=1)
    return tomorrow.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()


def resolve_zen(af=0):
    fam = {4: socket.AF_INET, 6: socket.AF_INET6}.get(af, socket.AF_UNSPEC)
    addrs = socket.getaddrinfo(ZEN_HOST, 443, fam, socket.SOCK_STREAM)
    ip = str(addrs[0][4][0])
    if ":" in ip:
        ip = f"[{ip}]"
    return f"https://{ip}{ZEN_PATH}", ZEN_HOST


class _BindAdapter(HTTPAdapter):
    def __init__(self, ip=None):
        self._ip = ip
        super().__init__()

    def init_poolmanager(self, *a, **kw):
        if self._ip:
            kw["source_address"] = (self._ip, 0)
        kw["server_hostname"] = ZEN_HOST
        kw["assert_hostname"] = ZEN_HOST
        return super().init_poolmanager(*a, **kw)


def _make_session(source_ip=None):
    s = requests.Session()
    adapter = _BindAdapter(source_ip)
    s.mount("http://", adapter)
    s.mount("https://", adapter)
    return s


def clean(payload):
    payload.setdefault("model", "deepseek-v4-flash-free")
    if "max_tokens" not in payload or payload["max_tokens"] > 65536:
        payload["max_tokens"] = 65536


class ZenProxy(http.server.BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Max-Age", "86400")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def _send(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self._cors()
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _proxy(self, method, path):
        client_ip = self.client_address[0]
        sv = cast(ThreadedServer, self.server)
        host = self.headers.get("Host", "")

        bl = getattr(sv, "banlist", None)
        if bl:
            if bl.is_banned(client_ip):
                return self._send(429, {"error": "Banned"})
            bl.incr(client_ip)

        auth = self.headers.get("Authorization", "")
        headers = {"Authorization": auth}
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length else None
        is_stream = False
        if body:
            payload = json.loads(body)
            clean(payload)
            is_stream = payload.get("stream", False)
            body = json.dumps(payload)
            headers["Content-Type"] = "application/json"

        mode = sv._mode_for_host(host)

        r = None
        last_error = None

        if mode == "v4":
            r = sv._try_family("v4", client_ip, body, headers, is_stream, method)
        elif mode == "v6":
            r = sv._try_family("v6", client_ip, body, headers, is_stream, method)
        else:
            families = ["v4", "v6"]
            random.shuffle(families)
            for fam in families:
                until = sv.cooldown.get(fam, 0)
                if until > time.time():
                    continue
                r = sv._try_family(fam, client_ip, body, headers, is_stream, method)
                if r is None:
                    sv.cooldown[fam] = next_utc_midnight()
                    continue
                if not is_stream:
                    try:
                        data = r.json()
                        if data.get("error", {}).get("type") == FREE_LIMIT_ERR:
                            last_error = data
                            sv.cooldown[fam] = next_utc_midnight()
                            r = None
                            continue
                    except (json.JSONDecodeError, ValueError):
                        pass
                break

        if r is None:
            if last_error:
                return self._send(429, last_error)
            return self._send(503, {"error": "All upstream IPs exhausted"})

        if is_stream:
            self.send_response(r.status_code)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self._cors()
            self.end_headers()
            for chunk in r.iter_content(chunk_size=None):
                if chunk:
                    try:
                        self.wfile.write(chunk)
                        self.wfile.flush()
                    except BrokenPipeError:
                        break
        else:
            self.send_response(r.status_code)
            self.send_header("Content-Type", "application/json")
            self._cors()
            self.end_headers()
            self.wfile.write(r.content)

    def do_POST(self):
        self._proxy("POST", "/chat/completions")

    def do_GET(self):
        if self.path == "/v1/models":
            self._proxy("GET", "/models")
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self._cors()
        self.end_headers()
        self.wfile.write(b"Zen proxy running\n")


class BanList:
    def __init__(self, max_reqs=MAX_REQS_PER_CLIENT, window=BAN_WINDOW):
        self._counts = {}
        self._banned = {}
        self._max = max_reqs
        self._window = window
        self._lock = threading.Lock()

    def incr(self, key):
        now = time.time()
        with self._lock:
            if key in self._banned:
                return
            cnt, t0 = self._counts.get(key, (0, now))
            if now - t0 > self._window:
                cnt = 0
                t0 = now
            cnt += 1
            if cnt > self._max:
                self._banned[key] = now + BAN_WINDOW
                self._counts.pop(key, None)
                return
            self._counts[key] = (cnt, t0)

    def is_banned(self, key):
        now = time.time()
        with self._lock:
            until = self._banned.get(key)
            if until is None:
                return False
            if now >= until:
                del self._banned[key]
                return False
            return True

    def unban(self, key):
        with self._lock:
            self._banned.pop(key, None)
            self._counts.pop(key, None)


class ThreadedServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, addr, port, handler):
        self.address_family = socket.AF_INET6 if ":" in addr else socket.AF_INET
        self._sessions: dict[str, tuple[requests.Session, float]] = {}
        self._sessions_lock = threading.Lock()
        self.cooldown: dict[str, float] = {}
        self.modes: dict[str, str] = {}
        self.banlist: BanList | None = None
        self.zen_base_v4: str = ""
        self.zen_host_v4: str = ""
        self.zen_base_v6: str = ""
        self.zen_host_v6: str = ""
        super().__init__((addr, port), handler)

    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if hasattr(socket, "SO_REUSEPORT"):
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        super().server_bind()

    def _mode_for_host(self, host):
        host = host.split(":")[0].lower()
        return self.modes.get(host, "v4")

    def get_session(self, key, ipv6=None):
        with self._sessions_lock:
            if key in self._sessions:
                return self._sessions[key][0]
            s = _make_session(ipv6)
            self._sessions[key] = (s, time.time())
            return s

    def _try_family(self, fam, client_ip, body, headers, is_stream, method):
        if fam == "v4":
            base, host = self.zen_base_v4, self.zen_host_v4
            session = self.get_session(f"v4:{client_ip}")
        else:
            base, host = self.zen_base_v6, self.zen_host_v6
            session = self.get_session(f"v6:{client_ip}")
        url = f"{base}{'/chat/completions' if body else '/models'}"
        hdrs = dict(headers)
        hdrs["Host"] = host
        for _ in range(2):
            try:
                r = session.request(method, url, data=body, headers=hdrs,
                                    stream=is_stream, timeout=TIMEOUT)
                return r
            except requests.exceptions.ConnectionError:
                pass
        return None

    def _cleanup(self):
        while True:
            time.sleep(CLEANUP_INTERVAL)
            now = time.time()
            with self._sessions_lock:
                stale = [k for k, v in self._sessions.items()
                         if now - v[1] > MAX_IDLE]
                for k in stale:
                    self._sessions.pop(k, None)

    def start_cleanup(self):
        t = threading.Thread(target=self._cleanup, daemon=True)
        t.start()


if __name__ == "__main__":
    addr = sys.argv[1] if len(sys.argv) > 1 else "0.0.0.0"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8443
    cert = sys.argv[3] if len(sys.argv) > 3 else None
    key = sys.argv[4] if len(sys.argv) > 4 else cert
    if len(sys.argv) > 5:
        TIMEOUT = int(sys.argv[5])
    server = ThreadedServer(addr, port, ZenProxy)
    server.banlist = BanList()

    server.zen_base_v4, server.zen_host_v4 = resolve_zen(4)
    server.zen_base_v6, server.zen_host_v6 = resolve_zen(6)

    server.modes = {
        "bwh4.d.moonchan.xyz": "v4",
        "bwh6.d.moonchan.xyz": "v6",
        "bwh.moonchan.xyz": "dual",
    }

    if cert:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(cert, key)
        server.socket = ctx.wrap_socket(server.socket, server_side=True)
        scheme = "https"
    else:
        scheme = "http"

    print(f"Zen proxy on {scheme}://{addr}:{port} (timeout={TIMEOUT}s)")
    server.serve_forever()
