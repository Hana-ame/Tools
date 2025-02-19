# coding=utf-8

import requests
import json
import os
import sys
import dotenv
from colorama import init, Fore, Back, Style
import pyperclip

init()  # 初始化，让颜色在所有终端生效

with open('content.txt', 'r', encoding='utf-8') as file:
  content = file.read()

dotenv.load_dotenv()
max_tokens = 8192
content = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else content


if __name__ == "__main__":
    url = "https://infer-modelarts-cn-southwest-2.modelarts-infer.com/v1/infers/861b6827-e5ef-4fa6-90d2-5fd1b2975882/v1/chat/completions"

    # Send request.
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer "
        + os.getenv("HUAWEI_API"),  # 把yourApiKey替换成真实的API Key
    }
    data = {
        "model": "DeepSeek-R1",
        "max_tokens": max_tokens - len(content) - len(os.getenv("SYSTEM_PROMPT")),
        "messages": [
            {"role": "system", "content": os.getenv("SYSTEM_PROMPT")},
            {"role": "user", "content": content},
        ],
        # 是否开启流式推理, 默认为False, 表示不开启流式推理
        "stream": False,
        # 在流式输出时是否展示使用的token数目。只有当stream为True时改参数才会生效。
        # "stream_options": { "include_usage": True },
        # 控制采样随机性的浮点数，值较低时模型更具确定性，值较高时模型更具创造性。"0"表示贪婪取样。默认为1.0。
        "temperature": 1.0,
    }
    resp = requests.post(
        url,
        headers=headers,
        data=json.dumps(data),
        timeout=3000,
        proxies={"http": None, "https": None},
        # verify=False,
    )

    # Print result.
    print(Fore.LIGHTBLACK_EX, resp.status_code, Style.RESET_ALL)
    print(Fore.GREEN, f"请求耗时：{resp.elapsed.total_seconds()} 秒", Style.RESET_ALL)
    if resp.status_code not in [200]:
        print(Fore.YELLOW, resp.json(), Style.RESET_ALL)
        exit(resp.status_code)
    print(resp.json()["choices"][0]["message"]["content"])
    pyperclip.copy(resp.json()["choices"][0]["message"]["content"])


def get_response_from_api(messages):
    """Function to send a request to the API with the provided messages."""
    url = "https://infer-modelarts-cn-southwest-2.modelarts-infer.com/v1/infers/861b6827-e5ef-4fa6-90d2-5fd1b2975882/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.getenv("HUAWEI_API"),  # Replace with actual API Key
    }
    
    # Calculate max_tokens dynamically based on the length of the content and system prompt
    data = {
        "model": "DeepSeek-R1",
        "max_tokens": max_tokens - sum(len(msg['content']) for msg in messages),
        "messages": messages,
        "stream": False,
        "temperature": 1.0,
    }
    
    # Send the request to the API
    resp = requests.post(
        url,
        headers=headers,
        data=json.dumps(data),
        timeout=3000,
        proxies={"http": None, "https": None},
    )

    # Return the response JSON object
    return resp.json()
