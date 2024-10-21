import os
import hashlib
import re

# def calculate_file_hash(file_path):
#   """计算单个文件的SHA-256哈希值"""
#   hash_sha256 = hashlib.sha256()
#   with open(file_path, 'rb') as f:
#     for byte_block in iter(lambda: f.read(4096), b""):
#       hash_sha256.update(byte_block)
#   return hash_sha256.hexdigest()

# def calculate_file_hash(file_path):
#     """计算文件的 MD5 哈希值"""
#     hash_md5 = hashlib.md5()
#     with open(file_path, "rb") as f:
#         for chunk in iter(lambda: f.read(4096), b""):
#             hash_md5.update(chunk)
#     return hash_md5.hexdigest()

def calculate_file_hash(file_path):
    """计算文件的 SHA-1 哈希值"""
    hash_sha1 = hashlib.sha1()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha1.update(chunk)
    return hash_sha1.hexdigest()

def sanitize_file_path(file_path):
    # 定义非法字符的正则表达式
    # 这里我们假设非法字符包括：\/:*?"<>|\\
    illegal_chars_pattern = r'[\/:*?"<>|\\]'
    
    # 使用 re.sub() 替换非法字符为下划线
    sanitized_path = re.sub(illegal_chars_pattern, '_', file_path)
    
    return sanitized_path



# # 未使用
# def calculate_folder_hash(folder_path):
#   """计算文件夹的哈希值"""
#   hash_sha256 = hashlib.sha256()
  
#   # 获取文件夹内所有文件的路径并排序
#   file_paths = []
#   for dirpath, dirnames, filenames in os.walk(folder_path):
#     print(dirpath, dirnames, filename)
#     for filename in filenames:
#       file_paths.append(os.path.join(dirpath, filename))

#   # 按照文件路径进行排序，确保一致性
#   file_paths.sort()
  
#   # 计算每个文件的哈希值，并更新文件夹的哈希值
#   for file_path in file_paths:
#     file_hash = calculate_file_hash(file_path)
#     hash_sha256.update(file_hash.encode('utf-8'))  # 将文件哈希值更新到文件夹哈希值中
  
#   return hash_sha256.hexdigest()

if __name__ == "__main__":
  # for test
  _ = calculate_file_hash(".gitignore")
  print(_)