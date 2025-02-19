import os
import time
from markdown import markdown
from datetime import datetime

def get_md_creation_time(md_path):
    """精确获取Markdown文件的创建时间戳（支持跨平台）"""
    try:
        # 优先使用元数据中的创建时间（如果存在）
        with open(md_path, 'r', encoding='utf-8') as f:
            first_line = f.readline()
            if first_line.startswith('<!-- Created:'):
                time_str = first_line.split(':').strip(' -->')
                return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S").timestamp()
    except:
        pass
    
    # 回退到文件系统元数据
    return os.path.getctime(md_path)

def compile_markdown_to_html(input_file, output_dir, css_url="https://cdn.example.com/minimal.css"):
    """增强版编译函数（自动注入时间戳）"""
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取原始MD信息
    md_creation = datetime.fromtimestamp(get_md_creation_time(input_file))
    time_header = f"<!-- Created: {md_creation.strftime('%Y-%m-%d %H:%M:%S')} -->\n"
    
    # 转换Markdown
    with open(input_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="{css_url}">
    {time_header}
</head>
<body>
    {markdown(md_content)}
</body>
</html>"""
    
    # 生成输出路径
    base_name = os.path.splitext(os.path.basename(input_file))
    output_path = os.path.join(output_dir, f"{base_name}.html")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return output_path, md_creation

def generate_sorted_index(input_dir, output_dir):
    """生成按MD创建时间排序的目录页"""
    # 遍历处理所有MD文件
    file_records = []
    for filename in os.listdir(input_dir):
        if filename.endswith('.md'):
            md_path = os.path.join(input_dir, filename)
            html_path, create_time = compile_markdown_to_html(md_path, output_dir)
            file_records.append((html_path, create_time))
    
    # 按MD创建时间降序排序
    sorted_files = sorted(file_records, key=lambda x: x, reverse=True)
    
    # 生成目录页
    index_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        .timestamp {{ color: #666; font-size: 0.9em; }}
        li {{ margin: 15px 0; }}
    </style>
</head>
<body>
    <h1>文章目录（按MD创建时间排序）</h1>
    <ul>
"""
    
    for html_path, create_time in sorted_files:
        title = os.path.splitext(os.path.basename(html_path))
        time_str = create_time.strftime("%Y-%m-%d %H:%M:%S")
        index_content += f'        <li><a href="{html_path}">{title}</a> <span class="timestamp">[{time_str}]</span></li>\n'
    
    index_content += """    </ul>
</body>
</html>"""
    
    index_path = os.path.join(output_dir, "index.html")
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"生成完成！目录文件：{index_path}")
    os.system(f'start {index_path}')  # 自动打开生成的目录

# 使用示例
if __name__ == "__main__":
    generate_sorted_index(
        input_dir="./markdown",  # 原始MD文件夹路径
        output_dir="./output"     # HTML输出目录
    )
