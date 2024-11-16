from dataclasses import dataclass, field
from datetime import datetime
from typing import List
import os
import hashlib
import yaml
import markdown

def compute_sha1(file_path: str) -> str:
    """计算给定文件的SHA1哈希值"""
    sha1 = hashlib.sha1()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):  # 逐块读取文件
            sha1.update(chunk)
    return sha1.hexdigest()

@dataclass
class FileMetadata:
    create_date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  # 创建日期
    edit_date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))    # 编辑日期
    sha1sum: str = ""  # 文件的SHA1哈希值
    filepath: str = ""  # 文件路径
    tags: List[str] = field(default_factory=list)  # 标签列表
    title: str = ""
    def to_dict(self):
        """将FileMetadata转换为字典，以便于JSON序列化"""
        return {
            "create_date": self.create_date,
            "edit_date": self.edit_date,
            "sha1sum": self.sha1sum,
            "filepath": self.filepath,
            "tags": self.tags,
            "title": self.title
        }


def get_file_metadata(file_path: str, tags: List[str]) -> FileMetadata:
    """获取文件的元数据，包括文件夹路径名作为标签"""
    # 检查文件扩展名
    _, file_extension = os.path.splitext(file_path)
    allowed_extensions = ['.md']  # 允许的扩展名列表
    if file_extension.lower() not in allowed_extensions:
        raise ValueError(f"文件扩展名 '{file_extension}' 不被允许。请使用以下扩展名之一: {', '.join(allowed_extensions)}")

    # 获取文件的创建时间和修改时间
    create_time = datetime.fromtimestamp(os.path.getctime(file_path)).strftime("%Y-%m-%d %H:%M")
    edit_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d %H:%M")

    # 计算文件的SHA1哈希值
    sha1sum = compute_sha1(file_path)

    # 读取文件的第一行以获取标题
    title = ""
    with open(file_path, 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()
        if first_line.startswith("# "):
            title = first_line[2:].strip()  # 提取标题内容


    # 创建FileMetadata实例
    file_metadata = FileMetadata(
        create_date=create_time,
        edit_date=edit_time,
        sha1sum=sha1sum,
        filepath=file_path,
        tags=tags,
        title=title # 添加标题
    )

    return file_metadata
def process_files_in_directory(directory: str, tags: List[str]) -> List[FileMetadata]:
    """处理指定目录中的所有文件并返回元数据"""
    metadata_list = []
    if os.path.isdir(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):  # 确保是文件
                try:
                    file_metadata = get_file_metadata(file_path, tags)
                    metadata_list.append(file_metadata)
                    
                except:
                    pass
    else:
        print(f"{directory} 不是一个有效的目录。")
    
    return metadata_list



# yaml

# read config
# see blog_example.yaml
def read_config(config_file: str) -> dict:
    """读取 YAML 配置文件"""
    with open(config_file, 'r', encoding='utf8') as file:
        config = yaml.safe_load(file)
    return config


#  markdown
def convert_md_to_html(md_file_path: str, output_html_path: str):
    """将 Markdown 文件转换为 HTML 并保存"""
    # 检查文件扩展名
    _, file_extension = os.path.splitext(md_file_path)
    if file_extension.lower() != '.md':
        raise ValueError("提供的文件不是一个 Markdown 文件。请确保文件扩展名为 .md")

    # 读取 Markdown 文件内容
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        md_content = md_file.read()

    # 转换为 HTML
    html_content = markdown.markdown(md_content)

    # 保存到 HTML 文件
    with open(output_html_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)

    print(f"已将 Markdown 文件 '{md_file_path}' 转换为 HTML 并保存为 '{output_html_path}'")

if __name__ == "__main__":
    
    # 使用示例
    md_file_path = 'example.md'  # 输入 Markdown 文件路径
    output_html_path = 'output.html'  # 输出 HTML 文件路径
    convert_md_to_html(md_file_path, output_html_path)
