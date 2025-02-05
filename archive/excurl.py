import sys
import os
import re
import requests
import time
import datetime
import pytz
from dotenv import load_dotenv
from requests.cookies import RequestsCookieJar

# 加载 .env 文件
load_dotenv()

# 记得自己填
cookie_str = os.getenv("COOKIE") or 'ipb_member_id=; ipb_pass_hash=; igneous='
headers = {"Cookie": cookie_str}
session = requests.Session()
session.headers.update(headers)

# 由于已经被SNI阻断，这个功能不再被使用
# iplist = ["178.175.128.252","178.175.132.22","178.175.128.254","178.175.129.254","178.175.132.20"]
# paras = ' -H "Host: exhentai.org" -k '
# def curl(href:str) -> str:
#     global iplist, cookie, paras
#     href = href.replace("exhentai.org",random.choice(iplist))
#     os.system(f'curl.exe --cookie "{cookie}" {paras} "{href}" -L -O -J')
#     print(href.split('/')[-1])
#     return href.split('/')[-1]

def is_within_time_range():
    """
    判断当前 UTC 时间是否在指定的时间范围内。

    Returns:
        如果当前时间在指定的时间范围内返回 `True`，否则返回 `False`。
    """

    # 获取当前 UTC 时间
    utc_now = datetime.datetime.now(pytz.utc)
    print(utc_now)
    # 获取当前 UTC 时间的小时、分钟和星期
    hour = utc_now.hour
    minute = utc_now.minute
    weekday = utc_now.weekday()  # 0 表示星期一，6 表示星期日

    if 0 <= weekday <= 5: #周一到周六
        if 14 <= hour < 20:
          return True
        else:
            return False
    elif weekday == 6: # 周日
         if 5 <= hour < 20 :
           return True
         else:
             return False
    else: # 不可能出现，只是为了逻辑严谨
      return False


def download(href:str) -> str:
    response = session.get(href)
    response.raise_for_status()
    txt = response.text
    fullimg = re.findall(r'https://exhentai.org/fullimg/[^"]+',txt)
    if not fullimg:
        fullimg = re.findall(r'<img id="img" src="([^"]+)"',txt)
    fullimg = fullimg[-1].replace('&amp;','&') 

    print(fullimg)
    img = session.get(fullimg)
    save_path = href.split("/")[-1]+'.'+fullimg.split('.')[-1]
    with open(save_path, "wb") as f:
        f.write(img.content)

    # curl(fullimg)
    next_href = re.findall(r'<a id="next" onclick="[^"]*?" href="([^"]*?)">',txt)
    if next_href:
        return next_href[0]
    return href
        

href =  "https://exhentai.org/s/2393884698/3189880-1"
print(sys.argv)
if len(sys.argv) > 1:
    href = sys.argv[1]

while href != '':
    time.sleep(10)
    if len(sys.argv) > 2 and is_within_time_range():
        continue
    nexthref = download(href)
    if href == nexthref:
        break
    href = nexthref
