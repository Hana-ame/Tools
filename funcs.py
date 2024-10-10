from typing import Dict
from pandas import Series
from .my_tools import load_json_files
# 导入替换用字典
data: Dict[str, Dict[str, str]] = load_json_files("dicts")

def sub(key: str, fn="default"):
  return (data.get(fn) or data.get("default") or {}).get(key, key)

def renew_lastrow(row: Series, lastrow: Series):
  # for cols in row.
  # if add or remove key, it will make errors (by gpt)
  # print(lastrow.index)
  for k in lastrow.index:
    # print(k)
    # print(k, row[k] , row[k] is None, lastrow[k] , lastrow[k] is None)
    lastrow[k] = row[k] or lastrow[k]
    # print(k, lastrow[k] is None)
  return lastrow