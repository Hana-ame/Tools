import os
import requests
import json

from dotenv import load_dotenv
load_dotenv()

response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": f"Bearer {os.getenv("TOKEN")}",
    "Content-Type": "application/json",
    # "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
    # "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
  },
  data=json.dumps({
    "model": "deepseek/deepseek-chat",
    "messages": [
      {
        "role": "user",
        "content": "带搜索的尝试是如何做出的"
      }
    ],
    
  })
)


print(json.dumps(response.json(), indent=2))
