# for show now time in obs
import time

import my_time
import my_file


while True:
    data = my_time.get_time_now_str()
    my_file.write_file("time.txt", "w", data)
    time.sleep(10)
