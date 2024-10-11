import subprocess
import sys
import os
import re
import json
from typing import Callable, List, Iterator


def set_title(title: str):
    subprocess.call(["echo", "-ne", f"\033]0;{title}\007"])
    # windows
    # subprocess.call(["title", title])


def parse_args(selector: Callable[[str], bool]) -> str | None:
    for arg in sys.argv:
        if selector(arg):
            return arg
    return None


def args_filter(function: Callable[[str], bool]) -> Iterator[str]:
    return filter(function, sys.argv)


def parse_fn(
    selector: Callable[[str], bool], parser: Callable[[str], str] = lambda x: x
) -> str | None:
    fn = os.path.basename(sys.argv[0])
    args = fn.split(".")
    args.reverse()
    for s in args:
        if selector(s):
            return parser(s)
    return None


def parse_startswith(s: str, prefix: str | List[str]) -> str | None:
    if isinstance(prefix, str):
        if s.startswith(prefix):
            return s[len(prefix) :]
        return None

    for p in prefix:
        if (string := parse_startswith(s, p)) is not None:
            return string
    return None


def parse_endswith(s: str, surfix: str | List[str]) -> str | None:
    if isinstance(surfix, str):
        if s.endswith(surfix):
            return s[: -len(surfix)]
        return None

    for p in surfix:
        if (string := parse_endswith(s, p)) is not None:
            return string
    return None


def load_json_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        # 加载 JSON 文件并更新到 data 字典
        json_data = json.load(f)
    return json_data


def load_json_files(folder_path):
    data = {}

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            fn = filename[: -len(".json")]
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                # 加载 JSON 文件并更新到 data 字典
                json_data = json.load(f)
                data[fn] = json_data

    return data


# def print_type(v: any):
#     print(type(v)) # <class 'function'>

if __name__ == "__main__":
    if (s := parse_startswith("__dsfsdf", ["123", "14", "__"])) is not None:
        print(s)
    else:
        print("s is None")

    if (s := parse_endswith("dsfsdf", ["123", "14", "__"])) is not None:
        print(s)
    else:
        print("s is None")

    if (s := parse_endswith("dsfsdf__", ["123", "14", "__"])) is not None:
        print(s)
    else:
        print("s is None")
