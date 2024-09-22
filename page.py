# toolkit for generating html

from utils import *



def generate_index(tags_list: List[str], metadata_list: List[FileMetadata], output_file: str):
    # 开始生成 HTML
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("<!DOCTYPE html>\n")
        f.write("<html lang='zh'>\n")
        f.write("<head>\n")
        f.write("<meta charset='UTF-8'>\n")
        f.write("<title>文章列表</title>\n")
        f.write("<style>\n")
        f.write("ul { list-style-type: none; padding: 0; }\n")
        f.write("li { display: inline; margin-right: 15px; }\n")  # 横向排列
        f.write("table { width: 100%; border-collapse: collapse; }\n")  # 表格宽度100%
        f.write("th, td { padding: 8px; }\n")  # 添加内边距，去掉边框
        f.write("td.title { width: 100%; }\n")  # 文章标题单元格宽度100%
        f.write("td.date { white-space: nowrap; }  /* 防止创建日期换行 */\n")
        f.write("</style>\n")
        f.write("</head>\n")
        f.write("<body>\n")
        
        # 生成标签目录
        f.write("<h2>标签目录</h2>\n")
        f.write("<ul>\n")
        for tag in tags_list:
            f.write(f"<li><a href='/tag/{tag}'>{tag}</a></li>\n")
        f.write("</ul>\n")

        # 生成文章列表
        f.write("<h2>文章列表</h2>\n")
        f.write("<table>\n")
        f.write("<tr><th>标题</th><th>创建日期</th></tr>\n")
        for metadata in metadata_list:
            f.write(f"<tr><td class='title'><a href='/article/{metadata.sha1sum}.html'>{metadata.title}</a></td><td class='date'>{metadata.create_date}</td></tr>\n")
        f.write("</table>\n")

        f.write("</body>\n")
        f.write("</html>\n")

if __name__ == "__main__":  
    # 模拟的元数据列表
    metadata_list = [
        FileMetadata(sha1sum="abc123", filepath="path/to/file1", tags=["Python", "编程"]),
        FileMetadata(sha1sum="def456", filepath="path/to/file2", tags=["JavaScript", "编程"]),
        FileMetadata(sha1sum="ghi789", filepath="path/to/file3", tags=["Python", "数据科学"]),
    ]

  # 生成 HTML 文件
    tags_list = ["main"]
    output_file_path = 'articles.html'
    generate_index(tags_list, metadata_list, output_file_path)
    print(f"已生成 HTML 文件：{output_file_path}")