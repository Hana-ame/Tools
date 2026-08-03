import datetime
import http.server
import itertools
import json
import os
import random
import signal
import socketserver
import sys
import threading
import time
import requests
from requests.adapters import HTTPAdapter

TIMEOUT = 120
CONNECT_TIMEOUT = 10
POOL_SIZE = 64
FREE_LIMIT_ERR = "FreeUsageLimitError"
COOLDOWN_SHORT = 60
BASE_MODEL = "deepseek-v4-flash-free"
MODEL_PREFIX = "deepseek-v4-flash"
INF_MODEL = "deepseek-v4-flash-inf"
INF_TOOL = "bash"
INF_TOOL_ARG = json.dumps({"command": "echo inf_loop_probe"})
INF_ROUNDS = 25

UPSTREAMS = [
    {"name": "bwh", "base": "https://bwh.moonchan.xyz:8443"},
    {"name": "vps", "base": "https://vps.moonchan.xyz:8443"},
    {"name": "cloudcone", "base": "https://cloudcone.moonchan.xyz:8443"},
]

ORDER = ["bwh", "vps", "cloudcone"]

_inf_lock = threading.Lock()
_inf_count = 0


def source_models():
    models = [{"id": BASE_MODEL, "name": f"DeepSeek V4 Flash (auto)"}]
    models.append({"id": INF_MODEL, "name": "DeepSeek V4 Flash (inf loop)"})
    models += [
        {"id": f"{MODEL_PREFIX}-{name}", "name": f"DeepSeek V4 Flash ({name})"}
        for name in ORDER
    ]
    return models


def resolve_model(model):
    if model == INF_MODEL:
        return None, BASE_MODEL
    if model and model != BASE_MODEL and model.startswith(MODEL_PREFIX + "-"):
        src = model[len(MODEL_PREFIX) + 1:]
        if src in ORDER:
            return src, BASE_MODEL
    return None, model


def next_utc_midnight():
    now = datetime.datetime.now(datetime.timezone.utc)
    tomorrow = now + datetime.timedelta(days=1)
    return tomorrow.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()


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


def _chunk_is_error(chunk):
    if not chunk:
        return False
    text = chunk.decode("utf-8", "ignore")
    low = text.lower()
    if '"error"' in text or "error type" in low:
        return True
    if "request queue is full" in low or "freeusagelimit" in low:
        return True
    return False


class Source:
    def __init__(self, name, base):
        self.name = name
        self.base = base
        self.session = requests.Session()
        self.session.trust_env = False
        adapter = HTTPAdapter(pool_connections=POOL_SIZE, pool_maxsize=POOL_SIZE)
        self.session.mount("https://", adapter)
        self.cooldown_until = 0.0
        self.last_err = ""
        self.reqs = 0


class MultiZen(http.server.BaseHTTPRequestHandler):
    sources: dict[str, Source] = {}

    def _log(self, msg):
        print(f"[{datetime.datetime.now().isoformat()}] {self.client_address[0]} - {msg}")

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Zen-Source")
        self.send_header("Access-Control-Max-Age", "86400")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def _send(self, status, data, ctype="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self._cors()
        self.end_headers()
        try:
            body = data if isinstance(data, bytes) else json.dumps(data).encode()
            self.wfile.write(body)
        except OSError:
            self._log("client disconnected during send")

    def _order(self, forced):
        order = list(ORDER)
        if forced and forced in order:
            order.remove(forced)
            random.shuffle(order)
            return [forced] + order
        random.shuffle(order)
        return order

    def _inf_inject(self):
        global _inf_count
        with _inf_lock:
            if _inf_count >= INF_ROUNDS:
                return None
            count = _inf_count + 1
            _inf_count = count
        call_id = f"call_inf_{count}"
        tool_evt = {
            "id": "inf",
            "object": "chat.completion.chunk",
            "created": 0,
            "model": BASE_MODEL,
            "choices": [{
                "index": 0,
                "delta": {
                    "tool_calls": [{
                        "index": 0,
                        "id": call_id,
                        "type": "function",
                        "function": {
                            "name": INF_TOOL,
                            "arguments": INF_TOOL_ARG,
                        },
                    }],
                },
                "finish_reason": None,
            }],
        }
        finish_evt = {
            "id": "inf",
            "object": "chat.completion.chunk",
            "created": 0,
            "model": BASE_MODEL,
            "choices": [{"index": 0, "delta": {}, "finish_reason": "tool_calls"}],
        }
        inject = (
            f"data: {json.dumps(tool_evt)}\n\n"
            f"data: {json.dumps(finish_evt)}\n\n"
        ).encode()
        self._log(f"injecting tool_call ({count}/{INF_ROUNDS})")
        return inject

    def _proxy(self, method, path, want_status=False):
        self._log(f"-> {method} {path}")
        auth = self.headers.get("Authorization", "")
        headers = {"Authorization": auth, "Connection": "close"}
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length else b""
        is_stream = False
        forced = None
        is_inf = False
        if body:
            payload = json.loads(body)
            is_inf = (payload.get("model") or BASE_MODEL) == INF_MODEL
            forced, model = resolve_model(payload.get("model") or BASE_MODEL)
            payload["model"] = model
            if "max_tokens" not in payload or payload["max_tokens"] > 65536:
                payload["max_tokens"] = 65536
            is_stream = payload.get("stream", False)
            self._log(f"req model={payload['model']} src={forced} max_tokens={payload['max_tokens']} stream={is_stream}")
            body_str = json.dumps(payload)
            headers["Content-Type"] = "application/json"
        else:
            body_str = ""

        header_src = (self.headers.get("X-Zen-Source") or "").strip()
        if header_src in self.sources:
            forced = header_src
        limit_error = None
        last_exc = None
        deadline = None
        for name in self._order(forced):
            src = self.sources[name]
            now = time.time()
            if src.cooldown_until > now:
                continue
            resp = None
            started = False
            try:
                url = src.base + ("/chat/completions" if body else "/v1/models")
                resp = src.session.request(
                    method, url, data=body_str, headers=headers,
                    stream=is_stream, timeout=(CONNECT_TIMEOUT, TIMEOUT)
                )
                if is_stream and resp.status_code == 200:
                    sock = _stream_socket(resp)
                    if sock is not None:
                        sock.settimeout(TIMEOUT)
                    else:
                        self._log(f"{name}: WARN could not resolve stream socket, using urllib3 default")
                    deadline = time.time() + TIMEOUT

                if resp.status_code != 200:
                    data = resp.json()
                    if data.get("error", {}).get("type") == FREE_LIMIT_ERR:
                        self._log(f"{name}: FreeUsageLimitError (cooldown to midnight)")
                        src.cooldown_until = next_utc_midnight()
                        src.last_err = "FreeUsageLimitError"
                        limit_error = data
                        resp.close()
                        continue
                    self._log(f"{name}: HTTP {resp.status_code} -> try next source")
                    src.last_err = f"HTTP {resp.status_code}"
                    resp.close()
                    continue

                src.reqs += 1
                src.last_err = ""
                if want_status:
                    resp.close()
                    continue

                if is_stream:
                    it = resp.iter_content(chunk_size=16384)
                    peek = []
                    for _ in range(20):
                        try:
                            peek.append(next(it))
                        except StopIteration:
                            break
                    if any(_chunk_is_error(c) for c in peek):
                        self._log(f"{name}: SSE error event, try next source")
                        src.last_err = "SSE error"
                        resp.close()
                        continue
                    chain = peek
                    rest = it
                else:
                    chain = [resp.content]
                    rest = iter([])

                self.send_response(resp.status_code)
                self.send_header(
                    "Content-Type",
                    "text/event-stream" if (is_stream and resp.status_code == 200) else "application/json",
                )
                self._cors()
                self.end_headers()
                started = True
                saw_tool = False
                for chunk in itertools.chain(chain, rest):
                    if deadline is not None and time.time() > deadline:
                        self._log(f"{name}: stream deadline exceeded, aborting")
                        resp.close()
                        self.close_connection = True
                        return
                    if not chunk:
                        continue
                    if is_stream and _chunk_is_error(chunk):
                        self._log(f"{name}: mid-stream error event dropped")
                        continue
                    if is_stream and b"tool_calls" in chunk:
                        saw_tool = True
                    out = chunk
                    if is_stream and is_inf and not saw_tool and b"[DONE]" in chunk:
                        before, _, done = chunk.partition(b"[DONE]")
                        if before.endswith(b"data: "):
                            before = before[:-len(b"data: ")]
                        out = before
                        if before:
                            try:
                                self.wfile.write(before)
                                self.wfile.flush()
                            except (BrokenPipeError, OSError):
                                self._log("client disconnected")
                                return
                        inject = self._inf_inject()
                        if inject:
                            try:
                                self.wfile.write(inject)
                                self.wfile.flush()
                            except (BrokenPipeError, OSError):
                                self._log("client disconnected")
                                return
                        self.wfile.write(b"data: [DONE]\n\n")
                        self.wfile.flush()
                        saw_tool = True
                        continue
                    try:
                        self.wfile.write(out)
                        self.wfile.flush()
                    except (BrokenPipeError, OSError):
                        self._log("client disconnected")
                        return
                resp.close()
                self._log(f"{name}: done (source={name})")
                return

            except requests.exceptions.RequestException as e:
                self._log(f"{name}: {type(e).__name__}")
                src.cooldown_until = time.time() + COOLDOWN_SHORT
                src.last_err = type(e).__name__
                if resp:
                    resp.close()
                if started:
                    self.close_connection = True
                    return
                last_exc = e
            except Exception as e:
                self._log(f"{name}: unexpected {e}")
                src.cooldown_until = time.time() + COOLDOWN_SHORT
                src.last_err = f"unexpected: {e}"
                if resp:
                    resp.close()
                if started:
                    self.close_connection = True
                    return
                last_exc = e

        if want_status:
            return
        if limit_error:
            return self._send(429, limit_error)
        if last_exc:
            self._log(f"all sources failed: {last_exc}")
        self._send(500, {"error": "所有上游源均不可用，请稍后重试"})

    def _status(self):
        rows = []
        for src in self.sources.values():
            rows.append({
                "name": src.name,
                "base": src.base,
                "cooldown_until": src.cooldown_until,
                "in_cooldown": src.cooldown_until > time.time(),
                "last_err": src.last_err,
                "reqs": src.reqs,
            })
        self._send(200, {"sources": rows})

    def do_POST(self):
        if self.path == "/status":
            return self._status()
        self._proxy("POST", "/chat/completions")

    def do_GET(self):
        if self.path == "/status":
            return self._status()
        if self.path == "/v1/models":
            return self._send(200, {
                "object": "list",
                "data": [
                    {"id": m["id"], "object": "model", "created": 0, "owned_by": "zen"}
                    for m in source_models()
                ],
            })
        self._send(200, b"Zen multi proxy running\n", ctype="text/plain")


class ThreadedServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8443

    signal.signal(signal.SIGHUP, signal.SIG_IGN)
    if os.name == "posix" and hasattr(signal, "SIGUSR1"):
        signal.signal(signal.SIGUSR1, signal.SIG_IGN)

    MultiZen.sources = {u["name"]: Source(u["name"], u["base"]) for u in UPSTREAMS}
    print("Zen multi proxy sources: " + ", ".join(MultiZen.sources))
    print("Models: " + ", ".join(m["id"] for m in source_models()))
    ThreadedServer((host, port), MultiZen).serve_forever()
