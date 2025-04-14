import datetime
import time


def get_time_now():
    now = datetime.datetime.now()
    return now

def get_time_now_str():
    now = get_time_now()
    now_str = f"{now.hour:02d}:{now.minute:02d}"
    return now_str

def formatted_time(format:str="%Y-%m-%d %H:%M:%S"):
    formatted_time = time.strftime(format)
    return formatted_time