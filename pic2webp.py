# coding:utf-8

from PIL import Image, ImageSequence 
import sys
import time 

def getpara(str):
  for c in str:
    if (c == 'q'):
      dest = 'quality'
    elif (c == 'm'):
      dest = 'method'
    elif (c == 'l'):
      if (dest != 'lossless'):
        dest = 'lossless'
      else:
        paras[dest] = True
    elif (c in ['0','1','2','3','4','5','6','7','8','9']):
      paras[dest] *= 10
      paras[dest] += int(c)
    else:
      print("有一些错误，请检查格式")
      paras['quality'] = 50
  if paras['quality'] > 100:
    print("quality 取0-100，已设置成 100 （越大质量越高）")
    paras['quality'] = 100
  if paras['method'] > 100:
    print("method 取0-6，已设置成 6 （越大压缩效果越好，速度越慢）")
    paras['method'] = 6
  print("使用的参数为")
  print("quality =",paras['quality'])
  print("method =",paras['method'])
  print("lossless =",paras['lossless'])

def progress(arg):
    im = Image.open(arg)
    seq = []
    for frame in ImageSequence.Iterator(im):
        seq.append(frame.copy())
    seq[0].save( arg + ".webp", save_all=True, append_images = seq[1:], quality=paras['quality'], method=paras['method'], lossless=paras['lossless'])

flag = 0
paras = {}
paras['quality'] = 0
paras['method'] = 0
paras['lossless'] = False

for arg in sys.argv:
    if flag == 0:            
        l = arg.split('.')
        flag += 1
        print(l[-2])
        getpara(l[-2])
        print("--------------------")
    else:
        try:
            print(arg)
            progress(arg)
            flag += 1
        except Exception as e:
            print(str(e))
            time.sleep(1)
        finally:
            pass

if (flag == 1):
    print("本程序使用方法为将希望转换的图片直接拖到图标上，你看起来是直接双击了程序")
else:
    print("已完成，10秒后将自动退出")
print("如有任何疑问请访问")
print("https://github.com/Hana-ame/Tools")
time.sleep(10)
