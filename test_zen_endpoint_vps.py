import subprocess
import json


def ssh_cmd(cmd):
    return subprocess.run(
        ["ssh", "root@vps.moonchan.xyz", cmd],
        capture_output=True, text=True, timeout=120
    )


def test_v4():
    print("=== vps.moonchan.xyz IPv4 -> opencode.ai/zen/v1/chat/completions ===")
    r = ssh_cmd(
        "curl -4 -s --max-time 30 -w '\\n%{http_code}\\t%{time_total}' "
        "'https://opencode.ai/zen/v1/chat/completions' "
        "-H 'Content-Type: application/json' "
        "-H 'Authorization: Bearer public' "
        "-d '{\"model\":\"deepseek-v4-flash-free\",\"messages\":[{\"role\":\"user\",\"content\":\"say hi\"}],\"max_tokens\":10}'"
    )
    lines = r.stdout.strip().split("\n")
    body = "\n".join(lines[:-1])
    meta = lines[-1] if len(lines) >= 2 else ""
    http_code, elapsed = meta.split("\t") if "\t" in meta else ("?", "?")
    print(f"  HTTP {http_code} | {elapsed}s")
    try:
        parsed = json.loads(body)
        print(f"  Response: {json.dumps(parsed, indent=2)}")
    except json.JSONDecodeError:
        print(f"  Response: {body[:500]}")
    print()


def test_v6():
    print("=== vps.moonchan.xyz IPv6 -> opencode.ai/zen/v1/chat/completions ===")
    r = ssh_cmd(
        "curl -6 -s --max-time 30 -w '\\n%{http_code}\\t%{time_total}' "
        "'https://opencode.ai/zen/v1/chat/completions' "
        "-H 'Content-Type: application/json' "
        "-H 'Authorization: Bearer public' "
        "-d '{\"model\":\"deepseek-v4-flash-free\",\"messages\":[{\"role\":\"user\",\"content\":\"say hi\"}],\"max_tokens\":10}'"
    )
    lines = r.stdout.strip().split("\n")
    body = "\n".join(lines[:-1])
    meta = lines[-1] if len(lines) >= 2 else ""
    http_code, elapsed = meta.split("\t") if "\t" in meta else ("?", "?")
    print(f"  HTTP {http_code} | {elapsed}s")
    try:
        parsed = json.loads(body)
        print(f"  Response: {json.dumps(parsed, indent=2)}")
    except json.JSONDecodeError:
        print(f"  Response: {body[:500]}")
    print()


def test_models():
    print("=== vps.moonchan.xyz IPv4 -> opencode.ai/zen/v1/models ===")
    r = ssh_cmd(
        "curl -4 -s --max-time 15 -w '\\n%{http_code}\\t%{time_total}' "
        "'https://opencode.ai/zen/v1/models'"
    )
    lines = r.stdout.strip().split("\n")
    body = "\n".join(lines[:-1])
    meta = lines[-1] if len(lines) >= 2 else ""
    http_code, elapsed = meta.split("\t") if "\t" in meta else ("?", "?")
    print(f"  HTTP {http_code} | {elapsed}s")
    if http_code == "200":
        parsed = json.loads(body)
        ids = [m["id"] for m in parsed["data"]]
        print(f"  Models ({len(ids)}): {', '.join(ids[:5])}...")
    print()


if __name__ == "__main__":
    test_models()
    test_v4()
    test_v6()
