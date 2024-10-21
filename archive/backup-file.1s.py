import os
import sys
import time
from utils import calculate_file_hash
import zipfile
from datetime import datetime

class MyArg:  
  def __init__(self, f: str) -> None:     
    self.second = 60
    self.minute = 0
    self.hour = 0    
    # 获取文件名
    fn = os.path.basename(f)
    for s in fn.split("."):
      if s.endswith('s'):
        try:
          self.second = int(s[:-1])
        except Exception:
          pass
      elif s.endswith('m'):
        try:
          self.minute = int(s[:-1])
        except Exception:
          pass
      elif s.endswith('h'):
        try:
          self.hour = int(s[:-1])
        except Exception:
          pass
  @property
  def duration(self):
    return self.hour*3600+self.minute*60+self.second

def back_file(fn : str):
  fn_list = fn.split('.')
  fn_list.pop()
  fn_list.append( datetime.now().strftime("%m-%d-%H-%M-%S"))
  fn_list.append('zip')
  zip_file_path = '.'.join(fn_list)
  # 创建 ZIP 文件并添加文件
  with zipfile.ZipFile(zip_file_path, 'w', compresslevel=9) as zipf:
    # 将文件添加到 ZIP 文件中
    zipf.write(fn, os.path.basename(fn))
  print(f"备份文件{os.path.basename(fn)}到{zip_file_path}")


arg = MyArg(sys.argv[0])
print(f"每间隔{arg.duration}秒检查一次")
print(f"文件有变动时，将变动后的文件备份")


hashmap = dict()

while True:
  for fn in sys.argv[1:]:
    if os.path.isdir(fn):
      continue
    
    sha1sum = calculate_file_hash(fn)
    if sha1sum != hashmap.get(fn):
      back_file(fn)
      hashmap[fn] = sha1sum
  print(f"上次检查时间 { datetime.now().strftime("%y-%m-%d-%H-%M-%S") }")
  time.sleep(arg.duration)

