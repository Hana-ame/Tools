
import os
from dataclasses import dataclass, asdict
import json5
from examples.e_dotenv import host,auth,id

@dataclass
class PostMessage:
  m: str
  tid: int
  bid: int
  n: str
  t: str
  id: str
  auth: str
  txt: str
  p: str
  page: int

  def to_json(self):
    return json5.dumps(asdict(self))

# 示例使用
def create_post_message(bid: int, tid: int, id: str, auth: str, url: str) -> PostMessage:
    return PostMessage(
        m="post",
        tid=tid,
        bid=bid,
        n="",
        t="",
        id=id,
        auth=auth,
        txt="post by post tool",
        p=url,
        page=0
    )

# 使用示例
# host = "https://getip.moonchan.xyz/echo"
bid = 102
tid = 133093
url = "https://file.moonchan.xyz/api/242981c55a9606770c493ae0d5656bd052f4afc7/vlcsnap-2023-04-13-21h26m48s974.png"

message = create_post_message(bid, tid, id, auth, url)
cmd = f"curl -X POST {host} -d '{message.to_json()}'"
print(cmd)
os.system(cmd)