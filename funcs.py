from typing import Dict
from .my_tools import load_json_files
# 导入替换用字典
data: Dict[str, Dict[str, str]] = load_json_files("dicts")

def sub(key: str, fn="default"):
  return (data.get(fn) or data.get("default") or {}).get(key, key)
