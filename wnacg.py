import json
import os

def rename(src, dst):
    # 定义源文件路径和目标路径
    # src = "path/to/source/file.txt"
    # dst = "path/to/destination/file.txt"

    # 移动文件（重命名）
    try:
        os.rename(src, dst)
        print(f"文件已从 {src} 移动到 {dst}")
    except FileNotFoundError:
        print(f"错误：源文件 {src} 不存在")
    except PermissionError:
        print(f"错误：权限不足，无法移动文件")
    except OSError as e:
        print(f"错误：{e}")


def rename_filename_in_url(item):
    """处理单个元素，重命名URL中的文件名"""
    url_parts = item['url'].split('/')
    old_filename = url_parts[-1]
    _, extension = os.path.splitext(old_filename)
    new_filename = f"{item['caption']}{extension}"
    url_parts[-1] = new_filename
    rename(old_filename, new_filename)
    return {
        "url": old_filename,
        "caption": new_filename,
    }

# 从文件加载JSON数据
file_path = "新建文本文档.txt"  # 确保文件路径正确
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)  # 假设文件内容是一个JSON列表
except FileNotFoundError:
    print(f"错误：文件 {file_path} 不存在")
    exit()
except json.JSONDecodeError:
    print("错误：文件内容不是有效的JSON格式")
    exit()

# 处理每个元素
processed_data = [rename_filename_in_url(item) for item in data]

# 打印结果（或保存到文件）
print("处理后的数据：")
print(json.dumps(processed_data, indent=2, ensure_ascii=False))

# 可选：保存到新文件
# with open("processed_data.json", 'w', encoding='utf-8') as f:
#     json.dump(processed_data, f, indent=2, ensure_ascii=False)
