def get_time_now():
    import datetime
    now = datetime.datetime.now()
    return now

def get_time_now_str():
    now = get_time_now()
    now_str = f"{now.hour:02d}:{now.minute:02d}"
    return now_str
