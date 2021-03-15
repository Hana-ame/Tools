# coding:utf-8

from PIL import Image 
import sys
import time 

def progress(arg):
    im = Image.open(arg)
    im.save( arg + ".webp", quality=50, method=6)

for arg in sys.argv:
        try:
            progress(arg)
        except Exception as e:
            print(str(e))
            time.sleep(0)
        finally:
            pass