# coding:utf-8

import sys
import time 

def progress(arg):
    f = open(arg,'rb')
    ct = f.read().decode('shift-jis').encode('UTF16')
    f.close()
    f = open(arg,'wb')
    f.write(ct)
    f.close()
    # end progress

for arg in sys.argv:
    if arg[-1] == 's':
        print(arg)
        try:
            progress(arg)
        except Exception as e:
            print(str(e))
            time.sleep(5)
        finally:
            pass