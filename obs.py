# for show now time in obs
import time

import my_time
import my_file
import my_tools

my_tools.title("写入时间到文本(obs)")

while True:
    data = my_time.get_time_now_str()
    my_file.write_file("time.txt", "w", data)
    time.sleep(10)
