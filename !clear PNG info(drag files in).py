# coding:utf-8

from PIL import Image 
import sys
import time 

def progress(arg):
    f = Image.open(arg) # open image
    f.save(arg)
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
