import base64

# 定义 Base64 编码的字符串
base64_string = "SGVsbG8sIFdvcmxkIQ=="  # 这是 "Hello, World!" 的 Base64 编码

# 解码 Base64 字符串
decoded_data = base64.b64decode(base64_string)

# 定义输出文件的路径
output_file_path = 'output.txt'  # 输出文件的路径

# 将解码后的数据写入文件
with open(output_file_path, 'wb') as output_file:
    output_file.write(decoded_data)

print(f"Base64 字符串已解码并保存到 {output_file_path}")