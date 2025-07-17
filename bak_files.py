import os
import sys
from my_tools import parse_endswith 

def invert_bytes_and_backup(file_path: str):
    i = 0
    # 生成备份文件名
    backup_path = f"{file_path}.bak1"
    backup_path = parse_endswith(backup_path, ".bak1.bak1") or backup_path
    try:
        # 打开原始文件和备份文件
        with open(file_path, 'rb') as src, open(backup_path, 'wb') as dst:
            while True:
                # 分块读取（默认1MB）
                chunk = src.read(1024 * 1024)
                if not chunk:
                    break
                # 对每个字节取反
                inverted = bytes([~b & 0xFF for b in chunk])  # 避免符号扩展问题[9,11](@ref)
                dst.write(inverted)
                print(" ", i, end='\r')
                i+=1
        print(f"备份成功：{backup_path}")
    
    except FileNotFoundError:
        print("原文件不存在")
    except PermissionError:
        print("权限不足")
    except Exception as e:
        print(f"未知错误：{e}")

# # 示例调用
# invert_bytes_and_backup(".env")
# invert_bytes_and_backup(".env.bak1")

for arg in sys.argv[1:]:
  invert_bytes_and_backup(arg)