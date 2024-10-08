import subprocess
import sys
import os
import re
from typing import Callable, List, Iterator

def set_title(title: str):
    subprocess.call(["echo", "-ne", f"\033]0;{title}\007"])
    # windows
    # subprocess.call(["title", title])

def parse_args(selector: Callable[[str], bool]) -> str:
    for arg in sys.argv:
        if selector(arg):
            return arg

def args_filter(function: Callable[[str], bool]) -> Iterator[str]:
    return filter(function, sys.argv)

def parse_fn(selector: Callable[[str], bool], parser: Callable[[str], str] = lambda x: x) -> str:
    fn = os.path.basename(sys.argv[0])
    for s in fn.split('.'):
        if selector(s):
            return parser(s)

        
# def print_type(v: any):
#     print(type(v)) # <class 'function'>

if __name__ == '__main__':
    pattern = r"hello$"
    pattern = r"world"
    string = "hello$ world"
    print(re.match(pattern, string) is False)
    print(re.search(pattern, string) is False)
    print(re.findall(pattern, string) is None)

    if re.search(pattern, string):
        print('...')
    
    s = parse_fn(lambda x: x.endswith('s'))
    print(s)

    s = args_filter(lambda x : True)
    print(s)
