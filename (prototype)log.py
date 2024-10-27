# what is this.

fn = '/home/admin/access.log'

def process_line(fn: str, fun: callable[[str], list[str]]):
  with open(fn) as f:
    f.read()
    arr = f.split('\n')
    return [fun(l) for l in arr]
  
def p(l):
  return l.split(' ')[0]

arr = process_line(fn, p)

data = '\n'.join(arr)

with open("/home/admin/highestip.txt", 'w') as f:
  f.write(data)
