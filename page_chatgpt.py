from dataclasses import dataclass, field
from typing import List
import os
import json
from datetime import datetime
import markdown
from utils import *  # Assuming the FileMetadata class is imported here
from compile_markdown_to_html import compile_markdown_to_html


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


def generate_index(tags_list: List[str], metadata_list: List[FileMetadata], output_file: str):
    """Generate a modern styled index HTML page"""
    with open(output_file, 'w', encoding='utf-8') as f:
        # Start HTML Structure
        f.write("<!DOCTYPE html>\n")
        f.write("<html lang='zh'>\n")
        f.write("<head>\n")
        f.write("<meta charset='UTF-8'>\n")
        f.write("<meta name='viewport' content='width=device-width, initial-scale=1.0'>\n")
        f.write("<title>文章列表</title>\n")
        f.write("<link rel='stylesheet' type='text/css' href='styles.css'>\n")  # External CSS file
        f.write("</head>\n")
        f.write("<body>\n")
        
        # Header Section
        f.write("<header>\n")
        f.write("<h1>文章目录</h1>\n")
        f.write("</header>\n")

        # Tag Directory
        f.write("<section class='tags-directory'>\n")
        f.write("<h2>标签目录</h2>\n")
        f.write("<ul>\n")
        for tag in tags_list:
            f.write(f"<li><a href='/tag/{tag}'>#{tag}</a></li>\n")
        f.write("</ul>\n")
        f.write("</section>\n")

        # Articles List
        f.write("<section class='articles-list'>\n")
        f.write("<h2>文章列表</h2>\n")
        f.write("<table>\n")
        f.write("<thead><tr><th>标题</th><th>创建日期</th><th>最后更新</th></tr></thead>\n")
        f.write("<tbody>\n")
        for metadata in metadata_list:
            f.write(f"<tr><td><a href='/article/{metadata.sha1sum}.html'>{metadata.title}</a></td><td>{metadata.create_date}</td><td>{metadata.edit_date}</td></tr>\n")
        f.write("</tbody>\n")
        f.write("</table>\n")
        f.write("</section>\n")
        
        # Footer Section
        f.write("<footer>\n")
        f.write("<p>© 2025 文章目录网站 | Designed by YourName</p>\n")
        f.write("</footer>\n")
        
        f.write("</body>\n")
        f.write("</html>\n")


# Markdown Conversion Function
md = markdown.Markdown(extensions=['fenced_code', 'codehilite', 'sane_lists', 'tables'])

def convert_md_to_html(title: str, md_file_path: str, output_html_path: str):
    """Convert a Markdown file to HTML and save it"""
    _, file_extension = os.path.splitext(md_file_path)
    if file_extension.lower() != '.md':
        raise ValueError("Provided file is not a Markdown file. Ensure the file extension is .md")

    # Read the markdown file content
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        md_content = md_file.read()

    # Convert to HTML
    html_content = md.convert(md_content)
    full_html_content = f"""<!DOCTYPE html>
<html lang='zh'>
<head>
    <meta charset='UTF-8'>
    <title>{title}</title>
    <link rel="stylesheet" type="text/css" href="/styles.css">  <!-- External CSS File -->
</head>
<body>
    {html_content}
</body>
</html>"""

    # Save to HTML file
    with open(output_html_path, 'w', encoding='utf-8') as html_file:
        html_file.write(full_html_content)

    print(f"Converted Markdown file '{md_file_path}' to HTML and saved as '{output_html_path}'")


if __name__ == "__main__":
    # Sample metadata list
    metadata_list = [
        FileMetadata(sha1sum="abc123", filepath="path/to/file1", title="Python 编程入门", create_date="2023-01-01", edit_date="2023-01-10", tags=["Python", "编程"]),
        FileMetadata(sha1sum="def456", filepath="path/to/file2", title="JavaScript 高级编程", create_date="2023-02-01", edit_date="2023-02-05", tags=["JavaScript", "编程"]),
        FileMetadata(sha1sum="ghi789", filepath="path/to/file3", title="数据科学与 Python", create_date="2023-03-01", edit_date="2023-03-10", tags=["Python", "数据科学"]),
    ]

    # Tags for the directory
    tags_list = ["编程", "数据科学", "Python"]

    # Generate the index HTML file
    output_file_path = 'articles.html'
    generate_index(tags_list, metadata_list, output_file_path)
    print(f"Generated HTML file: {output_file_path}")
