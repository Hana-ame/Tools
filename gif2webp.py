# coding:utf-8

from PIL import Image, ImageSequence 
import sys
import time 

def progress(arg):
    im = Image.open(arg)
    seq = []
    for frame in ImageSequence.Iterator(im):
        seq.append(frame.copy())
    seq[0].save( arg + ".webp", save_all=True, append_images = seq[1:], quality=50, method=6)

for arg in sys.argv:
    try:
        progress(arg)
    except Exception as e:
        print(str(e))
        time.sleep(1)
    finally:
        pass