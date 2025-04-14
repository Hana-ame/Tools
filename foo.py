import time
import my_time

i = 0
while i<4:
    time.sleep(1)
    print(f'i={i} "{time.ctime()}" - {my_time.formatted_time()}')
    i+=1