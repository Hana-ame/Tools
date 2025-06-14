import os
import requests
import json

from dotenv import load_dotenv
load_dotenv()

response = requests.get(
  url="https://openrouter.ai/api/v1/auth/key",
  headers={
    "Authorization": f"Bearer {os.getenv("TOKEN")}"
  }
)

print(json.dumps(response.json(), indent=2))
