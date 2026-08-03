import datetime
import http.server
import json
import socket
import ssl
import socketserver
import sys
import threading
import os
import time
import requests

AI_HOST = "generativelanguage.googleapis.com"
AI_PATH = "/v1beta/openai"
API_KEY = os.environ.get("AI_API_KEY", "")
TIMEOUT = 120
CONNECT_TIMEOUT = 10
CLEANUP_INTERVAL = 300
MAX_REQS_PER_CLIENT = 200
BAN_WINDOW = 600
POOL_SIZE = 50


def _make_session():
    s = requests.Session()
    adapter = requests.adapters.HTTPAdapter(pool_connections=POOL_SIZE, pool_maxsize=POOL_SIZE)
    s.mount("http://", adapter)
    s.mount("https://", adapter)
    return s


def set_socket_timeout(resp, timeout):
    try:
        raw = resp.raw._original_response.fp.raw._sock
        raw.settimeout(timeout)
    except Exception:
        pass


class AistudioProxy(http.server.BaseHTTPRequestHandler):
    def _log(self, msg):
        print(f"[{datetime.datetime.now().isoformat()}] {self.client_address[0]} - {msg}", flush=True)

    def log_message(self, fmt, *args):
        self._log(f"{fmt % args}")

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Max-Age", "86400")

    def do_OPTIONS(self):
        try:
            self.send_response(204)
            self._cors()
            self.end_headers()
        except OSError:
            pass

    def _send(self, status, data):
        try:
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self._cors()
            self.end_headers()
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

        headers = {"Authorization": f"Bearer {API_KEY}", "Connection": "close"}
        content_length = int(self.headers.get("Content-Length", 0))
        self._log(
            f"req: ua={self.headers.get('User-Agent', '')!r} "
            f"ctype={self.headers.get('Content-Type')} len={content_length} "
            f"accept={self.headers.get('Accept')} enc={self.headers.get('Accept-Encoding')}"
        )

        try:
            body = self.rfile.read(content_length) if content_length else b""
        except Exception as e:
            self._log(f"read body error: {e}")
            return self._send(400, {"error": "Bad Request"})

        is_stream = False
        if body:
            try:
                payload = json.loads(body)
            except json.JSONDecodeError:
                self._log("invalid JSON")
                return self._send(400, {"error": "Invalid JSON"})
            is_stream = payload.get("stream", False)
            headers["Content-Type"] = "application/json"
            self._log(
                f"body: model={payload.get('model')!r} stream={is_stream} "
                f"max_tokens={payload.get('max_tokens')} messages={len(payload.get('messages', []))} "
                f"tools={len(payload.get('tools') or [])} stream_options={payload.get('stream_options')}"
            )

        resp = None
        try:
            url = sv.ai_url + ("/chat/completions" if body else "/models")
            t0 = time.time()
            resp = sv.session.request(
                method, url, data=body, headers=headers,
                stream=is_stream, timeout=(CONNECT_TIMEOUT, TIMEOUT)
            )
            self._log(f"upstream {resp.status_code} in {time.time() - t0:.2f}s")
            if is_stream and resp.status_code == 200:
                set_socket_timeout(resp, TIMEOUT)

            if resp.status_code != 200:
                self._log(f"upstream {resp.status_code}")
                try:
                    data = resp.json()
                except Exception:
                    data = {}
                if resp.status_code == 429:
                    self._send(429, data)
                else:
                    self._send(resp.status_code, data)
                resp.close()
                return

            if not is_stream:
                try:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self._cors()
                    self.end_headers()
                    self.wfile.write(resp.content)
                    self._log("non-stream done")
                except OSError:
                    self._log("client disconnected during send")
                finally:
                    resp.close()
                return

            try:
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Cache-Control", "no-cache")
                self.send_header("Connection", "keep-alive")
                self._cors()
                self.end_headers()

                first_chunk = None
                total = 0
                for chunk in resp.iter_content(chunk_size=None):
                    if chunk:
                        if first_chunk is None:
                            first_chunk = time.time()
                            self._log(f"first byte +{first_chunk - t0:.2f}s")
                        total += len(chunk)
                        self.wfile.write(chunk)
                        self.wfile.flush()
                self._log(f"stream done ({total} bytes, ttft={first_chunk - t0 if first_chunk is not None else -1:.2f}s, total={time.time() - t0:.2f}s)")
            except (BrokenPipeError, OSError):
                self._log(f"client disconnected mid-stream ({total} bytes, {time.time() - t0:.2f}s)")
            finally:
                resp.close()

        except Exception as e:
            self._log(f"upstream error: {type(e).__name__} - {e}")
            if resp:
                resp.close()
            try:
                self._send(502, {"error": {"message": "Bad Gateway", "type": str(e)}})
            except Exception:
                pass

    def do_POST(self):
        self._proxy("POST", "/chat/completions")

    def do_GET(self):
        if self.path == "/v1/models":
            self._proxy("GET", "/models")
            return
        elif self.path in ("/status", "/health"):
            try:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self._cors()
                self.end_headers()
                now = time.time()
                status_data = {
                    "status": "ok",
                    "banned_ips": len(self.server.banlist._banned) if self.server.banlist else 0,
                    "active_threads": threading.active_count()
                }
                self.wfile.write(json.dumps(status_data).encode())
            except OSError:
                pass
            return

        try:
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self._cors()
            self.end_headers()
            self.wfile.write(b"Aistudio proxy running\n")
        except OSError:
            pass


class BanList:
    def __init__(self, max_reqs=MAX_REQS_PER_CLIENT, window=BAN_WINDOW):
        self._counts = {}
        self._banned = {}
        self._max = max_reqs
        self._window = window
        self._lock = threading.Lock()
        threading.Thread(target=self._cleanup_loop, daemon=True).start()

    def _cleanup_loop(self):
        while True:
            time.sleep(CLEANUP_INTERVAL)
            now = time.time()
            with self._lock:
                expired_bans = [k for k, v in self._banned.items() if now >= v]
                for k in expired_bans:
                    del self._banned[k]
                expired_counts = [k for k, v in self._counts.items() if now - v[1] > self._window]
                for k in expired_counts:
                    del self._counts[k]

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


class ThreadedServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, addr, port, handler):
        self.address_family = socket.AF_INET6 if ":" in addr else socket.AF_INET
        self.banlist: BanList | None = None
        self.ai_url: str = ""
        self.session = _make_session()
        self._ssl_ctx: ssl.SSLContext | None = None
        super().__init__((addr, port), handler)

    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        super().server_bind()

    def get_request(self):
        sock, addr = self.socket.accept()
        sock.settimeout(TIMEOUT)
        if self._ssl_ctx:
            try:
                sock = self._ssl_ctx.wrap_socket(sock, server_side=True)
            except Exception as e:
                sock.close()
                raise OSError(f"SSL handshake error: {e}")
        return sock, addr


if __name__ == "__main__":
    addr = sys.argv[1] if len(sys.argv) > 1 else "0.0.0.0"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 2053
    cert = sys.argv[3] if len(sys.argv) > 3 else None
    key = sys.argv[4] if len(sys.argv) > 4 else cert
    if len(sys.argv) > 5:
        TIMEOUT = int(sys.argv[5])

    banlist = BanList()

    s = ThreadedServer(addr, port, AistudioProxy)
    s.banlist = banlist
    s.ai_url = f"https://{AI_HOST}{AI_PATH}"

    if cert:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(cert, key)
        s._ssl_ctx = ctx
    print(f"Aistudio proxy on {'https' if cert else 'http'}://0.0.0.0:{port} (timeout={TIMEOUT}s)")
    s.serve_forever()
