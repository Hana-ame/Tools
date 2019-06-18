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
