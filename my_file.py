def write_file(fn: str, mode: str, data: str):
    with open(fn, mode) as f:
        f.write(data)


def open_and_read(fn: str) -> str:
    with open(fn) as f:
        return f.read()


# encoding is fixed to
class FilePrinter:
    def __init__(self, fn, encoding="utf8"):
        self.f = open(fn, "w", encoding=encoding)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.close()

    def print(self, s: str):
        self.f.write(s)

    def println(self, s=""):
        self.print(s + "\n")

    def close(self):
        self.f.close()
