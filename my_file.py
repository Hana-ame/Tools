def write_file(fn: str, mode: str, data: str):
    with open(fn, mode) as f:
        f.write(data)
        
def open_and_read(fn: str) -> str:
  with open(fn) as f:
    return f.read()
      
