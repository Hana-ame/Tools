import datetime
import http.server
import json
import queue
import socket
import ssl
import socketserver
import sys
import threading
import time
import requests
from requests.adapters import HTTPAdapter
import urllib3.util.connection

ZEN_HOST = "opencode.ai"
ZEN_PATH = "/zen/v1"
ZEN_API_KEY = "public"
TIMEOUT = 120
CONNECT_TIMEOUT = 10
STALL_TIMEOUT = 30
TOOL_STALL_TIMEOUT = 180
CLEANUP_INTERVAL = 300
MAX_IDLE = 3600
MAX_REQS_PER_CLIENT = 200
BAN_WINDOW = 600
FREE_LIMIT_ERR = "FreeUsageLimitError"
POOL_SIZE = 50

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


def _has_real_sse(buf):
    """True when a buffer/event carries real SSE data (`data:` or `event:`),
    as opposed to pure keep-alive comment lines (`: ...`)."""
    return b"data:" in buf or b"event:" in buf


def _event_has_tool_call(ev):
    """True only when the SSE event actually carries a real tool_call delta."""
    for line in ev.split(b"\n"):
        if not line.startswith(b"data: "):
            continue
        try:
            obj = json.loads(line[len(b"data: "):].decode("utf-8", "ignore"))
        except Exception:
            continue
        if not isinstance(obj, dict):
            continue
        for ch in obj.get("choices") or []:
            delta = ch.get("delta") or {}
            if delta.get("tool_calls"):
                return True
    return False


_STOP = object()
_ERR = object()


class _ThreadedIter:
    """Iterable consumed by a single persistent daemon worker thread.

    Consumers wait on a queue with a timeout; the worker never races the
    generator the way _timed_next did (which could hit "generator already
    executing" when a timed-out call looped again on the same iterable).
    """

    def __init__(self, it):
        self._q = queue.Queue()
        self._err = None

        def run():
            try:
                for chunk in it:
                    self._q.put(chunk)
                self._q.put(_STOP)
            except BaseException as e:
                self._err = e
                self._q.put(_ERR)

        threading.Thread(target=run, daemon=True).start()

    def next(self, timeout):
        try:
            item = self._q.get(timeout=timeout)
        except queue.Empty:
            return ("timeout", None)
        if item is _STOP:
            return ("stop", None)
        if item is _ERR:
            return ("err", self._err)
        return ("chunk", item)


def _close_resp(resp):
    """Close an upstream response without draining a still-open SSE stream.

    `resp.close()` can block forever when the upstream keeps sending keep-alive
    data (http.client tries to drain the connection). Close the underlying SSL
    socket first so every close returns immediately.
    """
    for getter in (
        lambda: resp.raw._original_response.fp.raw._sock,
        lambda: resp.raw._fp.fp.raw._sock,
        lambda: resp.raw._fp.raw._sock,
    ):
        try:
            s = getter()
            if s is not None:
                s.close()
                break
        except Exception:
            continue
    try:
        conn = resp.raw.connection
        if conn is not None:
            conn.close()
    except Exception:
        pass


class ZenProxy(http.server.BaseHTTPRequestHandler):
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

        auth = self.headers.get("Authorization", "")
        headers = {"Authorization": f"Bearer {ZEN_API_KEY}"}
        content_length = int(self.headers.get("Content-Length", 0))
        self._log(
            f"req: ua={self.headers.get('User-Agent', '')!r} "
            f"auth={'Bearer ' + auth[7:16] + '...' if auth.startswith('Bearer ') else repr(auth)} "
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

            payload.setdefault("model", "deepseek-v4-flash-free")
            if payload.get("model") == "deepseek-v4-flash":
                payload["model"] = "deepseek-v4-flash-free"
                self._log("model deepseek-v4-flash -> deepseek-v4-flash-free")
            if "max_tokens" not in payload or payload["max_tokens"] > 65536:
                payload["max_tokens"] = 65536
            if "top_p" in payload:
                tp = payload["top_p"]
                if not isinstance(tp, (int, float)) or not (0 < tp <= 1.0):
                    payload["top_p"] = 1.0
                    self._log(f"top_p {tp!r} out of range (0,1], clamped to 1.0")
            if "temperature" in payload:
                t = payload["temperature"]
                if not isinstance(t, (int, float)) or not (0 <= t <= 2.0):
                    payload["temperature"] = 1.0
                    self._log(f"temperature {t!r} out of range [0,2], reset to 1.0")
            is_stream = payload.get("stream", False)
            body_str = json.dumps(payload)
            headers["Content-Type"] = "application/json"
            self._log(
                f"body: model={payload.get('model')!r} stream={is_stream} "
                f"max_tokens={payload.get('max_tokens')} messages={len(payload.get('messages', []))} "
                f"tools={len(payload.get('tools') or [])} stream_options={payload.get('stream_options')}"
            )
        else:
            body_str = ""

        limit_error = None
        last_error = None
        last_status = None
        last_err_body = None
        headers_sent = False

        for fam, session in [("v6", sv.session_v6), ("v4", sv.session_v4)]:
            if sv.cooldown.get(fam, 0) > time.time():
                continue

            resp = None
            try:
                url = sv.zen_url + ("/chat/completions" if body else "/models")
                t0 = time.time()
                resp = session.request(
                    method, url, data=body_str, headers=headers,
                    stream=is_stream, timeout=(CONNECT_TIMEOUT, STALL_TIMEOUT)
                )
                tt = time.time() - t0
                self._log(f"{fam} upstream {resp.status_code} in {tt:.2f}s")
                if is_stream and resp.status_code == 200:
                    set_socket_timeout(resp, TIMEOUT)

                if not is_stream or resp.status_code != 200:
                    data = {}
                    raw_body = ""
                    try:
                        data = resp.json()
                    except Exception:
                        try:
                            raw_body = resp.text[:500]
                        except Exception:
                            raw_body = ""
                    if data.get("error", {}).get("type") == FREE_LIMIT_ERR:
                        self._log(f"{fam} FreeUsageLimitError")
                        limit_error = data
                        sv.cooldown[fam] = next_utc_midnight()
                        if resp:
                            _close_resp(resp)
                        continue
                    if resp.status_code != 200:
                        err = data.get("error") if isinstance(data, dict) else None
                        if isinstance(err, dict):
                            msg = err.get("message")
                            etype = err.get("type")
                            code = err.get("code")
                        else:
                            msg = data if data else None
                            etype = code = None
                        if not isinstance(msg, str):
                            msg = json.dumps(msg, ensure_ascii=False) if msg else None
                        last_error = msg or etype or code or (raw_body or f"HTTP {resp.status_code}")
                        last_status = resp.status_code
                        last_err_body = data or {"error": {"message": last_error}}
                        self._log(f"{fam} upstream {resp.status_code} error: {last_error}")
                        if resp:
                            _close_resp(resp)
                        continue

                if not is_stream:
                    try:
                        self.send_response(200)
                        self.send_header("Content-Type", "application/json")
                        self._cors()
                        self.end_headers()
                        headers_sent = True
                        self.wfile.write(resp.content)
                        self._log("non-stream done")
                    except OSError:
                        self._log("client disconnected during send")
                    finally:
                        if resp:
                            _close_resp(resp)
                    return

                try:
                    ti = _ThreadedIter(resp.iter_content(chunk_size=None))
                    pre = b""
                    t_pre = time.time()
                    while time.time() - t_pre < STALL_TIMEOUT and not _has_real_sse(pre):
                        kind, val = ti.next(STALL_TIMEOUT - (time.time() - t_pre))
                        if kind == "timeout":
                            break
                        if kind == "stop":
                            break
                        if kind == "err":
                            self._log(f"{fam} pre-read error: {type(val).__name__} - {val}")
                            break
                        if val:
                            pre += val
                    if not _has_real_sse(pre):
                        self._log(f"{fam} no real data in {STALL_TIMEOUT:.0f}s, try other stack")
                        if resp:
                            _close_resp(resp)
                        continue
                    first_chunk = time.time()
                    total = len(pre)
                    self._log(f"{fam} first real data +{first_chunk - t0:.2f}s")
                    self.send_response(200)
                    self.send_header("Content-Type", "text/event-stream")
                    self.send_header("Cache-Control", "no-cache")
                    self.send_header("Connection", "keep-alive")
                    self._cors()
                    self.end_headers()
                    headers_sent = True
                    last_real = time.time()
                    buf = pre
                    saw_tool = False
                    while True:
                        stall = TOOL_STALL_TIMEOUT if saw_tool else STALL_TIMEOUT
                        if time.time() - last_real > stall:
                            self._log(f"{fam} stream stalled (no real data {stall:.0f}s, saw_tool={saw_tool}), closing")
                            if not saw_tool:
                                try:
                                    self.wfile.write(b'data: {"error": {"message": "upstream stalled", "type": "UpstreamStall"}}\n\ndata: [DONE]\n\n')
                                    self.wfile.flush()
                                except (BrokenPipeError, OSError):
                                    pass
                            break
                        kind, val = ti.next(stall - (time.time() - last_real))
                        if kind == "timeout":
                            continue
                        if kind == "stop":
                            break
                        if kind == "err":
                            self._log(f"{fam} mid-stream error: {type(val).__name__} - {val}")
                            break
                        chunk = val
                        if not chunk:
                            continue
                        buf += chunk
                        while True:
                            i2 = buf.find(b"\n\n")
                            i4 = buf.find(b"\r\n\r\n")
                            if i4 != -1 and (i2 == -1 or i4 < i2):
                                ev, buf = buf[:i4], buf[i4 + 4:]
                            elif i2 != -1:
                                ev, buf = buf[:i2], buf[i2 + 2:]
                            else:
                                break
                            if not _has_real_sse(ev):
                                continue
                            if _event_has_tool_call(ev):
                                saw_tool = True
                            last_real = time.time()
                            total += len(ev) + 2
                            self.wfile.write(ev + b"\n\n")
                            self.wfile.flush()
                    self._log(f"{fam} stream done ({total} bytes, ttft={first_chunk - t0:.2f}s, total={time.time() - t0:.2f}s)")
                except (BrokenPipeError, OSError):
                    self._log(f"client disconnected mid-stream ({total} bytes, {time.time() - t0:.2f}s)")
                finally:
                    if resp:
                        _close_resp(resp)
                return

            except Exception as e:
                self._log(f"{fam} error: {type(e).__name__} - {e}")
                if resp:
                    _close_resp(resp)
                if headers_sent:
                    return

        if limit_error:
            return self._send(429, limit_error)

        if sv.cooldown.get("v4", 0) > time.time() and sv.cooldown.get("v6", 0) > time.time():
            return self._send(429, {"error": {"message": "All IPs have reached the daily free usage limit", "type": FREE_LIMIT_ERR}})

        if last_err_body is not None:
            if not isinstance(last_err_body, dict):
                last_err_body = {"error": {"message": str(last_err_body)}}
            if "error" not in last_err_body:
                last_err_body = {"error": {"message": last_err_body}}
            if isinstance(last_err_body.get("error"), dict) and "type" not in last_err_body["error"]:
                last_err_body["error"]["type"] = "UpstreamError"
            self._send(last_status or 502, last_err_body)
            return

        self._send(503, {"error": {"message": "All upstream IPs exhausted or unavailable", "type": "UpstreamError"}})

    def do_POST(self):
        self._proxy("POST", "/chat/completions")

    def do_GET(self):
        now = time.time()
        sv = self.server
        status_data = {
            "path": self.path,
            "server": sv.server_id,
            "status": "ok",
            "v4_cooldown_sec": max(0, int(sv.cooldown.get("v4", 0) - now)),
            "v6_cooldown_sec": max(0, int(sv.cooldown.get("v6", 0) - now)),
            "banned_ips": len(sv.banlist._banned) if sv.banlist else 0,
            "active_threads": threading.active_count()
        }
        try:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._cors()
            self.end_headers()
            self.wfile.write(json.dumps(status_data).encode())
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
        self.zen_url: str = ""
        self.server_id: str = "unknown"
        self.session_v4 = _make_session(socket.AF_INET)
        self.session_v6 = _make_session(socket.AF_INET6)
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
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8443
    cert = sys.argv[3] if len(sys.argv) > 3 else None
    key = sys.argv[4] if len(sys.argv) > 4 else cert
    if len(sys.argv) > 5:
        TIMEOUT = int(sys.argv[5])
    server_id = sys.argv[6] if len(sys.argv) > 6 else "unknown"

    banlist = BanList()

    s = ThreadedServer(addr, port, ZenProxy)
    s.banlist = banlist
    s.zen_url = f"https://{ZEN_HOST}{ZEN_PATH}"
    s.server_id = server_id

    if cert:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(cert, key)
        s._ssl_ctx = ctx
    print(f"Zen proxy on {'https' if cert else 'http'}://0.0.0.0:{port} (timeout={TIMEOUT}s)")
    s.serve_forever()
