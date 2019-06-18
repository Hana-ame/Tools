# coding:utf-8

from PIL import Image 
import sys
import time 

def progress(arg):
    png = Image.open(arg) # open image
    arg = arg[:-4] + '.jpg'
    if png.mode == 'RGBA':
        png.load() # required for png.split()
        background = Image.new("RGB", png.size, (255, 255, 255))
        background.paste(png, mask=png.split()[3]) # 3 is the alpha channel
        background.save(arg, "JPEG", quality=80)
    else:
        png.save(arg, "JPEG", quality=80)
    f = open(arg,'ab')
    f.write(bytes('\r\nThe massage below is written with UTF-8!!\r\n翻译/嵌字：花飴\r\ntranslating/editing:Anemone|HanaAme\r\n此版本为压缩过的jpg格式图片，仅供在http://67.218.132.205在线试阅','utf-8'))
    f.close()

for arg in sys.argv:
    if arg[-4:] == '.png':
        print(arg)
        try:
            progress(arg)
        except Exception as e:
            print(str(e))
            time.sleep(5)
        finally:
            pass