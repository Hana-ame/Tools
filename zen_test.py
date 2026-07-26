import requests
import json

BASE = "https://opencode.ai/zen/v1"
API_KEY = "public"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

r = requests.get(f"{BASE}/models", headers=HEADERS)
print("=== Free Models ===")
data = r.json()
free = [m["id"] for m in data["data"] if "free" in m["id"]]
for i, m in enumerate(free, 1):
    print(f"  {i}. {m}")

model = free[0]
print(f"\nUsing: {model} | Context: 1M | API Key: {API_KEY}\n")
print("Type 'exit' to quit, '!models' to switch model\n")

messages = []
while True:
    user = input("You: ")
    if user.lower() in ("exit", "quit"):
        break
    if user == "!models":
        for i, m in enumerate(free, 1):
            print(f"  {i}. {m}")
        idx = int(input("Select #: ")) - 1
        model = free[idx]
        print(f"Switched to {model}")
        continue

    messages.append({"role": "user", "content": user})
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": 65536,
    }
    r = requests.post(f"{BASE}/chat/completions", json=payload, headers=HEADERS)
    if r.status_code != 200:
        print(f"Error {r.status_code}: {r.text[:200]}")
        messages.pop()
        continue

    data = r.json()
    msg = data["choices"][0]["message"]
    reasoning = msg.get("reasoning_content", "")
    content = msg["content"] or ""
    if reasoning:
        print(f"Reasoning: {reasoning}")
    print(f"AI: {content}")
    messages.append({"role": "assistant", "content": content or reasoning})
