
from collections import defaultdict
from io import TextIOWrapper
import sys

def green_text(s: str) -> str:
    return "\033[92m" + str(s) + "\033[0m"

fn = sys.argv[1]

def lines(f: TextIOWrapper):
  l = f.readline()
  while l:
    yield l
    l = f.readline()

d = defaultdict(int)
def add(key: str):
  d[key] += 1

with open(fn) as f:
  for l in lines(f):
    ll = l.split("\"")
    add(ll[-2])

cnt = 0
for key in d:
  # print(key,'\t\t' ,d[key])
  if d[key] > 100:
    cnt+=1

sorted_kv = sorted(d.items(), key=lambda x: x[0])
for key, value in sorted_kv:
    print(key, green_text(value))



