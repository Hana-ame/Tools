import json
import http.server
import socketserver
import threading
import requests
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BACKENDS = ["bwh", "vps", "cloudcone"]
TIMEOUT = 120
CONNECT_TIMEOUT = 10
POOL_SIZE = 50
ATTEMPTS = 3


def _stream_socket(resp):
    for getter in (
        lambda: resp.raw._original_response.fp.raw._sock,
        lambda: resp.raw._fp.fp.raw._sock,
        lambda: resp.raw._fp.raw._sock,
        lambda: resp.raw.connection.sock,
    ):
        try:
            s = getter()
            if s is not None:
                return s
        except Exception:
            continue
    return None

session = requests.Session()
session.verify = False
session.trust_env = False
for scheme in ("http://", "https://"):
    session.mount(scheme, requests.adapters.HTTPAdapter(
        pool_connections=POOL_SIZE, pool_maxsize=POOL_SIZE
    ))


class LocalProxy(http.server.BaseHTTPRequestHandler):
    def _log(self, msg):
        print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Max-Age", "86400")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        if self.path == "/v1/models":
            self._proxy("GET", self.path)
            return
        self.send_response(200)
        self._cors()
        self.end_headers()
        self.wfile.write(b"Local proxy running\n")

    def do_POST(self):
        self._proxy("POST", self.path)

    def _send(self, status, data):
        try:
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self._cors()
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        except OSError:
            self._log("client disconnected")

    def _proxy(self, method, path):
        t_start = time.time()
        content_length = int(self.headers.get("Content-Length", 0))
        self._log(f"-> {method} {path} len={content_length}")
        self.connection.settimeout(60)
        body = self.rfile.read(content_length) if content_length else b""
        headers = {k: v for k, v in self.headers.items() if k.lower() in (
            "authorization", "content-type"
        )}
        headers["Connection"] = "close"

        is_stream = False
        if body:
            try:
                payload = json.loads(body)
                is_stream = payload.get("stream", False)
            except json.JSONDecodeError:
                pass

        last_error = None
        for host in BACKENDS:
            url = f"https://{host}.moonchan.xyz:8443/zen/v1/chat/completions"
            for attempt in range(ATTEMPTS):
                resp = None
                started = False
                self._log(f"-> {host} attempt {attempt+1}")
                try:
                    resp = session.request(
                        method, url, data=body, headers=headers,
                        stream=is_stream, timeout=(CONNECT_TIMEOUT, TIMEOUT)
                    )

                    if resp.status_code == 500:
                        last_error = f"{host} 500"
                        resp.close()
                        continue

                    if resp.status_code != 200:
                        last_error = f"{host} returned {resp.status_code}"
                        resp.close()
                        break

                    deadline = None
                    if is_stream:
                        sock = _stream_socket(resp)
                        if sock is not None:
                            sock.settimeout(TIMEOUT)
                        else:
                            self._log(f"{host}: WARN could not resolve stream socket, using urllib3 default")
                        deadline = time.time() + TIMEOUT

                    self.send_response(200)
                    self.send_header(
                        "Content-Type",
                        "text/event-stream" if is_stream else "application/json",
                    )
                    self.send_header("Cache-Control", "no-cache")
                    self.send_header("Connection", "close")
                    self._cors()
                    self.end_headers()
                    started = True

                    if is_stream:
                        total = 0
                        for chunk in resp.iter_content(chunk_size=16384):
                            if deadline is not None and time.time() > deadline:
                                self._log(f"{host}: stream idle timeout, aborting")
                                resp.close()
                                self.close_connection = True
                                self._log("FAIL")
                                return
                            if not chunk:
                                continue
                            deadline = time.time() + TIMEOUT
                            total += len(chunk)
                            try:
                                self.wfile.write(chunk)
                                self.wfile.flush()
                            except OSError:
                                self._log("client disconnected")
                                resp.close()
                                self._log("FAIL")
                                return
                        resp.close()
                        self._log(
                            f"{host}: stream done {total}B tt={time.time() - t_start:.2f}s"
                        )
                    else:
                        self.wfile.write(resp.content)
                        self.wfile.flush()
                        resp.close()
                        self._log(f"{host}: 200 tt={time.time() - t_start:.2f}s")
                    return

                except requests.exceptions.RequestException as e:
                    self._log(f"{host} error: {type(e).__name__} - {e}")
                    last_error = str(e)
                    if resp:
                        resp.close()
                    if started:
                        self.close_connection = True
                        self._log("FAIL")
                        return

        self._send(503, {"error": f"All backends failed: {last_error}"})


class ThreadedServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    server = ThreadedServer(("127.0.0.1", 11434), LocalProxy)
    print(f"Local proxy on http://127.0.0.1:11434/v1/chat/completions")
    print(f"Backends: {', '.join(f'{h}.moonchan.xyz:8443' for h in BACKENDS)}")
    server.serve_forever()
