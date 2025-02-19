import markdown
from pathlib import Path

def compile_markdown_to_html(title: str, input_file, output_file=".", css_url="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown.min.css"):
    """
    将Markdown文件编译为带样式的HTML文件
    参数：
        input_file: 输入的.md文件路径
        output_dir: 输出目录（默认当前目录）
        css_url: 可选的CSS URL（默认使用GitHub风格CSS）
    """
    # 读取Markdown内容
    md_content = Path(input_file).read_text(encoding="utf-8")
    
    # 配置Markdown扩展（支持表格、任务列表等）
    extensions = [
        'tables',                # 表格支持
        'pymdownx.tasklist',     # 待办事项列表
        'pymdownx.superfences',  # 代码块增强
        'mdx_math'               # 数学公式支持
    ]
    
    # 转换为HTML
    html_content = markdown.markdown(
        md_content,
        extensions=extensions,
        output_format='html5'
    )
    
    # 构建完整HTML文档
    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{Path(input_file).stem}</title>
    <link rel="stylesheet" href="{css_url}">
    <style>
        .markdown-body {{
            box-sizing: border-box;
            min-width: 200px;
            max-width: 980px;
            margin: 0 auto;
            padding: 45px;
        }}
        @media (max-width: 767px) {{
            .markdown-body {{
                padding: 15px;
            }}
        }}
        /* 自定义待办事项样式 */
        .task-list-item-checkbox {{
            margin: 0 0.2em 0.25em -1.4em;
            vertical-align: middle;
        }}
    </style>
</head>
<body class="markdown-body">
    {html_content}
</body>
</html>"""
    
    # 确保输出目录存在
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 写入文件
    output_path.write_text(full_html, encoding="utf-8")

if __name__ == '__main__':
  # 使用示例
  compile_markdown_to_html(
      input_file="demo.md",
      output_dir="./output",
      # 使用自定义CSS可改为本地路径如："styles.css"
  )


# def compile_markdown_to_html(input_file, output_dir=".", css_url="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown.min.css"):
#     """
#     将Markdown文件编译为带样式的HTML文件
#     参数：
#         input_file: 输入的.md文件路径
#         output_dir: 输出目录（默认当前目录）
#         css_url: 可选的CSS URL（默认使用GitHub风格CSS）
#     """
#     # 读取Markdown内容
#     md_content = Path(input_file).read_text(encoding="utf-8")
    
#     # 配置Markdown扩展（支持表格、任务列表等）
#     extensions = [
#         'tables',                # 表格支持
#         'pymdownx.tasklist',     # 待办事项列表
#         'pymdownx.superfences',  # 代码块增强
#         'mdx_math'               # 数学公式支持
#     ]
    
#     # 转换为HTML
#     html_content = markdown.markdown(
#         md_content,
#         extensions=extensions,
#         output_format='html5'
#     )
    
#     # 构建完整HTML文档
#     full_html = f"""<!DOCTYPE html>
# <html>
# <head>
#     <meta charset="utf-8">
#     <title>{Path(input_file).stem}</title>
#     <link rel="stylesheet" href="{css_url}">
#     <style>
#         .markdown-body {{
#             box-sizing: border-box;
#             min-width: 200px;
#             max-width: 980px;
#             margin: 0 auto;
#             padding: 45px;
#         }}
#         @media (max-width: 767px) {{
#             .markdown-body {{
#                 padding: 15px;
#             }}
#         }}
#         /* 自定义待办事项样式 */
#         .task-list-item-checkbox {{
#             margin: 0 0.2em 0.25em -1.4em;
#             vertical-align: middle;
#         }}
#     </style>
# </head>
# <body class="markdown-body">
#     {html_content}
# </body>
# </html>"""
    
#     # 确保输出目录存在
#     output_path = Path(output_dir)
#     output_path.mkdir(parents=True, exist_ok=True)
    
#     # 写入文件
#     output_file = output_path / f"{Path(input_file).stem}.html"
#     output_file.write_text(full_html, encoding="utf-8")
#     return str(output_file)

# if __name__ == '__main__':
#   # 使用示例
#   compile_markdown_to_html(
#       input_file="demo.md",
#       output_dir="./output",
#       # 使用自定义CSS可改为本地路径如："styles.css"
#   )
