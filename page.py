from typing import List
from utils import *  # 假设这里导入了 FileMetadata 类

def generate_index(tags_list: List[str], metadata_list: List[FileMetadata], output_file: str):
    # 开始生成 HTML
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("<!DOCTYPE html>\n")
        f.write("<html lang='zh'>\n")
        f.write("<head>\n")
        f.write("<meta charset='UTF-8'>\n")
        f.write("<meta name='viewport' content='width=device-width, initial-scale=1.0'>\n")  # 添加视口标签
        f.write("<title>文章列表</title>\n")
        f.write("<link rel='stylesheet' type='text/css' href='styles.css'>\n")
        f.write("</head>\n")
        f.write("<body>\n")
        f.write("<div class='container'>\n")  # 添加容器包裹内容
        
        # 生成标签目录
        f.write("<section class='tags-section'>\n")
        f.write("<h2>📁 标签目录</h2>\n")
        f.write("<div class='tag-list'>\n")
        for tag in tags_list:
            f.write(f"<a class='tag-item' href='/tag/{tag}'>{tag}</a>\n")
        f.write("</div>\n")
        f.write("</section>\n")

        # 生成文章列表
        f.write("<section class='articles-section'>\n")
        f.write("<h2>📝 最新文章</h2>\n")
        f.write("<div class='table-container'>\n")  # 表格容器用于响应式
        f.write("<table class='article-table'>\n")
        f.write("<thead><tr><th>标题</th><th>创建日期</th><th>最后更新</th></tr></thead>\n")
        f.write("<tbody>\n")
        for metadata in metadata_list:
            f.write(f"<tr><td><a class='article-title' href='/article/{metadata.sha1sum}.html'>{metadata.title}</a></td>"
                    f"<td class='date'>{metadata.create_date}</td><td class='date'>{metadata.edit_date}</td></tr>\n")
        f.write("</tbody>\n")
        f.write("</table>\n")
        f.write("</div>\n")
        f.write("</section>\n")

        f.write("</div>\n")  # 容器结束
        f.write("</body>\n")
        f.write("</html>\n")

#  markdown

# 启用 fenced_code 和 codehilite 选项
md = markdown.Markdown(extensions=['fenced_code', 'codehilite', "sane_lists", "tables"])

def convert_md_to_html(title: str, md_file_path: str, output_html_path: str):
    """将 Markdown 文件转换为 HTML 并保存"""
    # 检查文件扩展名
    _, file_extension = os.path.splitext(md_file_path)
    if file_extension.lower() != '.md':
        raise ValueError("提供的文件不是一个 Markdown 文件。请确保文件扩展名为 .md")

    # 读取 Markdown 文件内容
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        md_content = md_file.read()

    # 转换为 HTML
    html_content = md.convert(md_content)
    full_html_content = f"""<!DOCTYPE html>
<html lang='zh'>
<head>
    <meta charset='UTF-8'>
    <title>{title}</title>
    <link rel="stylesheet" type="text/css" href="/styles.css">  <!-- 引用外部 CSS 文件 -->
</head>
<body>
    {html_content}
</body>
</html>"""

    # 保存到 HTML 文件
    with open(output_html_path, 'w', encoding='utf-8') as html_file:
        html_file.write(full_html_content)

    print(f"已将 Markdown 文件 '{md_file_path}' 转换为 HTML 并保存为 '{output_html_path}'")

if __name__ == "__main__":    
    # 使用示例
    md_file_path = 'example.md'  # 输入 Markdown 文件路径
    output_html_path = 'output.html'  # 输出 HTML 文件路径
    convert_md_to_html(md_file_path, output_html_path)


if __name__ == "__main__":  
    # 模拟的元数据列表
    metadata_list = [
        FileMetadata(sha1sum="abc123", filepath="path/to/file1", title="Python 编程入门", create_date="2023-01-01", last_updated="2023-01-10", tags=["Python", "编程"]),
        FileMetadata(sha1sum="def456", filepath="path/to/file2", title="JavaScript 高级编程", create_date="2023-02-01", last_updated="2023-02-05", tags=["JavaScript", "编程"]),
        FileMetadata(sha1sum="ghi789", filepath="path/to/file3", title="数据科学与 Python", create_date="2023-03-01", last_updated="2023-03-10", tags=["Python", "数据科学"]),
    ]

    # 生成 HTML 文件
    tags_list = ["main"]
    output_file_path = 'articles.html'
    generate_index(tags_list, metadata_list, output_file_path)
    print(f"已生成 HTML 文件：{output_file_path}")