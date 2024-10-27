from PIL import Image 
import sys
import time 

def progress(arg):
    # open image
    f = Image.open(arg) 
    # 创建一个同样大小的画布
    im = Image.new( mode = f.mode, size = f.size )
    # 几个参数
    w,h = f.size
    l = [0,0,0,0,0,0,0,0,0,0,0]
    for i in range(10):
        l[i] = h//10*i
    l[10] = h
    # 从下往上绘图
    for i in range(10):
        frag = f.crop((0, l[i], w, l[i+1]))
        im.paste(frag, (0, h-l[i+1], w, h-l[i]))
    # save
    im.save(arg, quality=95)



for arg in sys.argv:
    if arg[-4:] == '.jpg':
        print(arg)
        try:
            progress(arg)
        except Exception as e:
            print(str(e))
            print("请报告该问题")
            time.sleep(5)
        finally:
            pass
    else:
        print("注意不支持PNG，如有需要请联系")

input('按回车键退出')