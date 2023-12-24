import subprocess

def title(title: str):
    subprocess.call(["echo", "-ne", f"\033]0;{title}\007"])
    # windows
    # subprocess.call(["title", title])
