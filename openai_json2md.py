import json
import sys
from pathlib import Path


def extract_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for p in content:
            if isinstance(p, str):
                parts.append(p)
            elif isinstance(p, dict):
                t = p.get("type")
                if t == "text":
                    parts.append(p.get("text", ""))
                elif t == "image_url":
                    url = p.get("image_url", {})
                    parts.append(f"![image]({url.get('url', '') if isinstance(url, dict) else url})")
                else:
                    parts.append(p.get("text", "") or json.dumps(p, ensure_ascii=False))
        return "\n".join(parts)
    return str(content)


def quote(text):
    return "\n".join("> " + line for line in text.splitlines())


def main():
    if len(sys.argv) < 2:
        print("usage: python openai_json2md.py input.json [output.md]")
        sys.exit(1)

    src = Path(sys.argv[1])
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_suffix(".md")
    data = json.loads(src.read_text(encoding="utf-8"))

    lines = []
    model = data.get("model", "")
    if model:
        lines.append(f"# {model}")
        lines.append("")

    for msg in data.get("messages", []):
        role = msg.get("role", "message")
        content = extract_text(msg.get("content", "")).strip()
        reasoning = msg.get("reasoning_content") or msg.get("reasoning")
        usage = msg.get("usage")

        lines.append(f"## {role.title()}")
        lines.append("")
        if reasoning:
            lines.append("### Reasoning")
            lines.append("")
            lines.append(quote(str(reasoning).strip()))
            lines.append("")
        if content:
            lines.append(content)
            lines.append("")
        if usage and role == "assistant":
            lines.append(f"*{json.dumps(usage, ensure_ascii=False)}*")
            lines.append("")

    dst.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"written: {dst} ({len(data.get('messages', []))} messages)")


if __name__ == "__main__":
    main()
