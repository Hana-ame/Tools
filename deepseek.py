# ddns

import requests
import os 
import dotenv
import json 
import socket 

def getIPv6():
    ipstr:str = None
    while ipstr is None:
        try:
            s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
            s.connect(('2001:da8:20d:22::2',80)) # edu.cn
            ipstr = s.getsockname()[0]
            s.close()
        except Exception as e:
            print(e)
    return ipstr

import time

dotenv.load_dotenv()


zone_id = os.getenv("ZONE_ID")  # 替换为实际值
record_id = os.getenv("DNS_RECORD_ID")
print(record_id)
cloudflare_email = os.getenv("CLOUDFLARE_EMAIL")  # 替换为Cloudflare邮箱
cloudflare_api_key = os.getenv("CLOUDFLARE_API_KEY")  # 替换为API密钥

def list_records():
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    headers = {
        "X-Auth-Email": cloudflare_email,
        "X-Auth-Key": cloudflare_api_key
    }

    response = requests.get(url, headers=headers)
    pretty_json = json.dumps(response.json(), indent=2, ensure_ascii=False, sort_keys=True)
    print(pretty_json)
    return response.json()

def update_record(record_id: str, ipv6:str):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Email": cloudflare_email,
        "X-Auth-Key": cloudflare_api_key,
    }
    
    data = {
        "type": "AAAA",
        "name": "desktop.d.moonchan.xyz",
        "content": ipv6,
        "ttl": 60,
        "proxied": False
    }
    
    response = requests.patch(
        url,     
        headers=headers,
        data=json.dumps(data),
        timeout=3000,
        proxies={"http": None, "https": None},
        # verify=False,
    )
    
    return response.json()

if __name__ == "__main__":
    while True:
      try:
        ip = getIPv6()
        print(ip)
        resp_json = update_record(record_id, ip)
        print(resp_json)
        time.sleep(60)
      except Exception as e:
        print(e)