import http.server
import json
import socket
import ssl
import socketserver
import sys
import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

ZEN_BASE = "https://opencode.ai/zen/v1"
TIMEOUT = 120

class _BindAdapter(HTTPAdapter):
    def __init__(self, ip=None):
        self._ip = ip
        super().__init__()
    def init_poolmanager(self, *a, **kw):
        if self._ip:
            kw["source_address"] = (self._ip, 0)
        return super().init_poolmanager(*a, **kw)

def _make_session(source_ip=None):
    s = requests.Session()
    adapter = _BindAdapter(source_ip)
    s.mount("http://", adapter)
    s.mount("https://", adapter)
    return s

SESSION = _make_session()

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

    def do_POST(self):
        body = self.rfile.read(int(self.headers["Content-Length"]))
        payload = json.loads(body)
        clean(payload)
        is_stream = payload.get("stream", False)

        auth = self.headers.get("Authorization", "")
        try:
            r = SESSION.post(
                f"{ZEN_BASE}/chat/completions",
                json=payload,
                headers={"Authorization": auth},
                stream=is_stream,
                timeout=TIMEOUT,
            )
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
                    self.wfile.flush()
            else:
                self.send_response(r.status_code)
                self.send_header("Content-Type", "application/json")
                self._cors()
                self.end_headers()
                self.wfile.write(r.content)
        except Exception as e:
            data = json.dumps({"error": str(e)}).encode()
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self._cors()
            self.end_headers()
            self.wfile.write(data)

    def do_GET(self):
        if self.path == "/v1/models":
            auth = self.headers.get("Authorization", "")
            try:
                r = SESSION.get(
                    f"{ZEN_BASE}/models",
                    headers={"Authorization": auth},
                    timeout=TIMEOUT,
                )
                data = r.content
                self.send_response(r.status_code)
            except Exception as e:
                data = json.dumps({"error": str(e)}).encode()
                self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self._cors()
            self.end_headers()
            self.wfile.write(data)
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self._cors()
        self.end_headers()
        self.wfile.write(b"Zen proxy running\n")

class ThreadedServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, addr, port, handler):
        self.address_family = socket.AF_INET6 if ":" in addr else socket.AF_INET
        super().__init__((addr, port), handler)

if __name__ == "__main__":
    addr = sys.argv[1] if len(sys.argv) > 1 else "::1"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8080
    cert = sys.argv[3] if len(sys.argv) > 3 else None
    if len(sys.argv) > 5:
        TIMEOUT = int(sys.argv[5])
    outbound_ip = sys.argv[6] if len(sys.argv) > 6 else None
    if outbound_ip:
        SESSION = _make_session(outbound_ip)
    server = ThreadedServer(addr, port, ZenProxy)
    if cert:
        key = sys.argv[4] if len(sys.argv) > 4 else cert
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(cert, key)
        server.socket = ctx.wrap_socket(server.socket, server_side=True)
        scheme = "https"
    else:
        scheme = "http"
    extra = f"timeout={TIMEOUT}s"
    if outbound_ip:
        extra += f", outbound_ip={outbound_ip}"
    print(f"Zen proxy on {scheme}://[{addr}]:{port} ({extra})")
    server.serve_forever()
