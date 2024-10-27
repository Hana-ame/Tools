# coding:utf-8

from PIL import Image 
import sys
import time 

def getpara(str):
    try:
        paras['quality'] = int(str)
    except:
        print("需要是一个0-100的整数，使用初始值进行转换")
        paras['quality'] = 80


def progress(arg):
    png = Image.open(arg).convert("RGB") # open image
    # arg = arg[:-4] + '.jpg'
    if png.mode == 'RGBA':
        png.load() # required for png.split()
        background = Image.new("RGB", png.size, (255, 255, 255))
        background.paste(png, mask=png.split()[3]) # 3 is the alpha channel
        background.save(arg+".jpg", "JPEG", quality=paras['quality'])
    else:
        png.save(arg+".jpg", "JPEG", quality=paras['quality'])
    f = open(arg,'ab')
    f.close()

flag = 0
paras = {}
paras['quality'] = 80

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
time.sleep(10)
