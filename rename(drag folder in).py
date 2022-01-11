import os
import sys

def renameitem(path,f):
 try:
  ff = f.encode('gbk').decode('shift-jis')
  # ff = f.encode('shift-jis').decode('gbk')
  if ff == f: return 
  print(f'move "{path}\\{f}" "{path}\\{ff}"')
  os.system(f'move "{path}\\{f}" "{path}\\{ff}"')
 except:
  print(f'fail {f}')
  pass

def rename(path):
 for p, folds, files in os.walk(path):
  for f in files:  
   renameitem(p,f)
#  for p, folds, files in os.walk(path):
  for f in folds:  
   renameitem(p,f)

def rename2(path):
 l = path.split('\\')
 renameitem('\\'.join(l[:-1]),l[-1])

for arg in sys.argv:
 print(arg.split('\\')[-1])
 rename(arg)
#  rename(f'.\\{arg}')
 rename2(arg)   
# path, folds, files = next(os.walk('.'))
# for f in folds: 
#  print(f) 
#  renameitem(path,f)


import time
time.sleep(999)



