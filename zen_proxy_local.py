import argparse
import datetime
import http.server
import json
import socket
import socketserver
import threading
import time
import requests
from requests.adapters import HTTPAdapter
import urllib3.util.connection

ZEN_HOST = "opencode.ai"
ZEN_PATH = "/zen/v1"
TIMEOUT = 120
CONNECT_TIMEOUT = 10
POOL_SIZE = 50
FREE_LIMIT_ERR = "FreeUsageLimitError"

_local = threading.local()


def _allowed_gai_family():
    try:
        return _local.family
    except AttributeError:
        return socket.AF_UNSPEC


urllib3.util.connection.allowed_gai_family = _allowed_gai_family


def next_utc_midnight():
    now = datetime.datetime.now(datetime.timezone.utc)
    tomorrow = now + datetime.timedelta(days=1)
    return tomorrow.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()


class FamilyAdapter(HTTPAdapter):
    def __init__(self, family, **kwargs):
        self._family = family
        super().__init__(**kwargs)

    def send(self, request, **kwargs):
        _local.family = self._family
        try:
            return super().send(request, **kwargs)
        finally:
            _local.family = socket.AF_UNSPEC


def _make_session(family):
    s = requests.Session()
    adapter = FamilyAdapter(family, pool_connections=POOL_SIZE, pool_maxsize=POOL_SIZE)
    s.mount("http://", adapter)
    s.mount("https://", adapter)
    return s


def set_socket_timeout(resp, timeout):
    try:
        raw = resp.raw._original_response.fp.raw._sock
        raw.settimeout(timeout)
    except Exception:
        pass


def ipv6_available(timeout=3):
    if not socket.has_ipv6:
        return False
    try:
        infos = socket.getaddrinfo(ZEN_HOST, 443, socket.AF_INET6, socket.SOCK_STREAM)
    except socket.gaierror:
        return False
    for family, socktype, proto, _, addr in infos[:3]:
        s = socket.socket(family, socktype, proto)
        s.settimeout(timeout)
        try:
            s.connect(addr)
            return True
        except OSError:
            pass
        finally:
            s.close()
    return False


class ZenProxyLocal(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _log(self, msg):
        print(f"[{datetime.datetime.now().isoformat()}] {self.client_address[0]} - {msg}")

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, PATCH, OPTIONS, HEAD")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Expose-Headers", "*")
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
        self._log(f"-> {method} {path}")

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
        for fam, session in [("v4", self.server.session_v4), ("v6", self.server.session_v6)]:
            if session is None:
                continue
            if self.server.cooldown.get(fam, 0) > time.time():
                continue
            resp = None
            try:
                url = self.server.zen_url + ("/chat/completions" if body else "/models")
                resp = session.request(
                    method, url, data=body_str, headers=headers,
                    stream=is_stream, timeout=(CONNECT_TIMEOUT, TIMEOUT)
                )
                if is_stream and resp.status_code == 200:
                    set_socket_timeout(resp, TIMEOUT)

                if not is_stream or resp.status_code != 200:
                    data = resp.json()
                    if data.get("error", {}).get("type") == FREE_LIMIT_ERR:
                        self._log(f"{fam} FreeUsageLimitError")
                        limit_error = data
                        self.server.cooldown[fam] = next_utc_midnight()
                        resp.close()
                        continue

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
        if self.path.split("?")[0] in ("/v1/models", "/models"):
            self._proxy("GET", "/models")
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self._cors()
        self.end_headers()
        try:
            self.wfile.write(b"Zen proxy (local dual-stack) running\n")
        except OSError:
            pass


class ThreadedServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, addr, port, handler):
        self.cooldown: dict[str, float] = {}
        self.zen_url: str = ""
        self.session_v4 = _make_session(socket.AF_INET)
        if ipv6_available():
            self.session_v6 = _make_session(socket.AF_INET6)
        else:
            self.session_v6 = None
        super().__init__((addr, port), handler)

    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        super().server_bind()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Local dual-stack Zen proxy")
    parser.add_argument("--port", "-p", type=int, default=8000, help="listen port (default 8000)")
    parser.add_argument("--timeout", type=int, default=None, help="upstream timeout in seconds (default 120)")
    args = parser.parse_args()
    if args.timeout:
        TIMEOUT = args.timeout

    addr = "0.0.0.0"
    port = args.port

    s = ThreadedServer(addr, port, ZenProxyLocal)
    s.zen_url = f"https://{ZEN_HOST}{ZEN_PATH}"
    print(f"Zen proxy (local dual-stack) on http://{addr}:{port} (timeout={TIMEOUT}s)")
    print(f"IPv6 upstream: {'enabled' if s.session_v6 else 'disabled (no local IPv6)'}")
    s.serve_forever()
