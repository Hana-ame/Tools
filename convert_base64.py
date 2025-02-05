# usage: py convert_base64.py [file] ...
# see output: [file].py

import os
import sys
import base64

def template(fn: bytes, data: bytes):
    return f"""import base64
base64_string = b"{data.decode()}"
decoded_data = base64.b64decode(base64_string)
output_file_path = '{fn}'

with open(output_file_path, 'wb') as output_file:
    output_file.write(decoded_data)""".encode()


def convert_to_py_file(fn: str):
    with open(fn, 'rb') as input_file:
        # 读取文件内容
        file_content = input_file.read()

        # 将文件内容编码为 Base64
        encoded_content = base64.b64encode(file_content)

    base_fn = os.path.basename(fn)

    with open(base_fn+'.py', 'wb') as output_file:
        output_file.write(template(base_fn, encoded_content))
    
    print(f"{fn} -> {base_fn}.py")

if __name__ == '__main__':
    for arg in sys.argv[1:]:
        convert_to_py_file(arg)

