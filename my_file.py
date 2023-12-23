def write_file(fn: str, mode: str, data: str):
    with open(fn, mode) as f:
        f.write(data)
