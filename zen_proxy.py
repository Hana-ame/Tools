import datetime
import http.server
import json
import socket
import ssl
import socketserver
import sys
import threading
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.connection import allowed_gai_family

ZEN_HOST = "opencode.ai"
ZEN_PATH = "/zen/v1"
TIMEOUT = 120
CONNECT_TIMEOUT = 10
CLEANUP_INTERVAL = 300
MAX_IDLE = 3600
MAX_REQS_PER_CLIENT = 200
BAN_WINDOW = 600
FREE_LIMIT_ERR = "FreeUsageLimitError"
POOL_SIZE = 50


def next_utc_midnight():
    now = datetime.datetime.now(datetime.timezone.utc)
    tomorrow = now + datetime.timedelta(days=1)
    return tomorrow.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()


def _make_session():
    s = requests.Session()
    adapter = HTTPAdapter(pool_connections=POOL_SIZE, pool_maxsize=POOL_SIZE)
    s.mount("http://", adapter)
    s.mount("https://", adapter)
    return s


def set_socket_timeout(resp, timeout):
    try:
        raw = resp.raw._original_response.fp.raw._sock
        raw.settimeout(timeout)
    except Exception:
        pass


class ZenProxy(http.server.BaseHTTPRequestHandler):
    def _log(self, msg):
        print(f"[{datetime.datetime.now().isoformat()}] {self.client_address[0]} - {msg}")

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
        try:
            self.wfile.write(json.dumps(data).encode())
        except OSError:
            self._log("client disconnected during send")

    def _proxy(self, method, path):
        client_ip = self.client_address[0]
        sv = self.server
        self._log(f"-> {method} {path}")

        if sv.banlist and sv.banlist.is_banned(client_ip):
            self._log("banned")
            return self._send(429, {"error": "Banned"})
        if sv.banlist:
            sv.banlist.incr(client_ip)

        auth = self.headers.get("Authorization", "")
        headers = {"Authorization": auth}
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length else b""
        is_stream = False
        if body:
            payload = json.loads(body)
            payload.setdefault("model", "deepseek-v4-flash-free")
            if "max_tokens" not in payload or payload["max_tokens"] > 65536:
                payload["max_tokens"] = 65536
            is_stream = payload.get("stream", False)
            body_str = json.dumps(payload)
            headers["Content-Type"] = "application/json"
        else:
            body_str = ""

        limit_error = None
        for fam, session in [("v4", sv.session_v4), ("v6", sv.session_v6)]:
            if sv.cooldown.get(fam, 0) > time.time():
                continue
            resp = None
            try:
                url = sv.zen_base[fam] + ("/chat/completions" if body else "/models")
                hdrs = dict(headers)
                hdrs["Host"] = sv.zen_host[fam]
                resp = session.request(
                    method, url, data=body_str, headers=hdrs,
                    stream=is_stream, timeout=(CONNECT_TIMEOUT, TIMEOUT)
                )
                if is_stream and resp.status_code == 200:
                    set_socket_timeout(resp, TIMEOUT)

                if not is_stream or resp.status_code != 200:
                    data = resp.json()
                    if data.get("error", {}).get("type") == FREE_LIMIT_ERR:
                        self._log(f"{fam} FreeUsageLimitError")
                        limit_error = data
                        sv.cooldown[fam] = next_utc_midnight()
                        resp.close()
                        continue

                # success
                if resp.status_code != 200:
                    self.send_response(resp.status_code)
                    self.send_header("Content-Type", "application/json")
                    self._cors()
                    self.end_headers()
                    self.wfile.write(resp.content)
                    return

                if not is_stream:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self._cors()
                    self.end_headers()
                    self.wfile.write(resp.content)
                    self._log("non-stream done")
                    return

                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Cache-Control", "no-cache")
                self.send_header("Connection", "keep-alive")
                self._cors()
                self.end_headers()
                for chunk in resp.iter_content(chunk_size=None):
                    if chunk:
                        try:
                            self.wfile.write(chunk)
                            self.wfile.flush()
                        except (BrokenPipeError, OSError):
                            self._log("client disconnected")
                            break
                self._log("stream done")
                return

            except requests.exceptions.ConnectionError:
                self._log(f"{fam} ConnectionError")
                if resp:
                    resp.close()
            except requests.exceptions.ReadTimeout:
                self._log(f"{fam} ReadTimeout")
                if resp:
                    resp.close()
            except OSError:
                self._log(f"{fam} OSError")
                if resp:
                    resp.close()
            except Exception as e:
                self._log(f"{fam} unexpected error: {e}")
                if resp:
                    resp.close()

        if limit_error:
            return self._send(429, limit_error)
        self._send(503, {"error": "All upstream IPs exhausted"})

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
        try:
            self.wfile.write(b"Zen proxy running\n")
        except OSError:
            pass


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
                cnt, t0 = 0, now
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
        self.cooldown: dict[str, float] = {}
        self.banlist: BanList | None = None
        self.zen_base: dict[str, str] = {}
        self.zen_host: dict[str, str] = {}
        self.session_v4 = _make_session()
        self.session_v6 = _make_session()
        self._ssl_ctx: ssl.SSLContext | None = None
        super().__init__((addr, port), handler)

    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        super().server_bind()

    def get_request(self):
        sock, addr = self.socket.accept()
        if self._ssl_ctx:
            sock.settimeout(10)
            try:
                sock = self._ssl_ctx.wrap_socket(sock, server_side=True)
            except OSError:
                sock.close()
                raise
            sock.settimeout(None)
        return sock, addr


def resolve_zen(af=0):
    fam = {4: socket.AF_INET, 6: socket.AF_INET6}.get(af, socket.AF_UNSPEC)
    addrs = socket.getaddrinfo(ZEN_HOST, 443, fam, socket.SOCK_STREAM)
    ip = str(addrs[0][4][0])
    if ":" in ip:
        ip = f"[{ip}]"
    return f"https://{ip}{ZEN_PATH}", ZEN_HOST


if __name__ == "__main__":
    addr = sys.argv[1] if len(sys.argv) > 1 else "0.0.0.0"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8443
    cert = sys.argv[3] if len(sys.argv) > 3 else None
    key = sys.argv[4] if len(sys.argv) > 4 else cert
    if len(sys.argv) > 5:
        TIMEOUT = int(sys.argv[5])

    banlist = BanList()
    zen_base_v4, zen_host_v4 = resolve_zen(4)
    zen_base_v6, zen_host_v6 = resolve_zen(6)

    s = ThreadedServer(addr, port, ZenProxy)
    s.banlist = banlist
    s.zen_base = {"v4": zen_base_v4, "v6": zen_base_v6}
    s.zen_host = {"v4": zen_host_v4, "v6": zen_host_v6}

    if cert:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(cert, key)
        s._ssl_ctx = ctx
    print(f"Zen proxy on {'https' if cert else 'http'}://0.0.0.0:{port} (timeout={TIMEOUT}s)")
    s.serve_forever()
