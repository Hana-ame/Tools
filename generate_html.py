import os

from natsort import natsorted

def generate_html(images, output_file="images.html"):
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>图片列表</title>
        <style>
            body { background: #f0f0f0; padding: 20px; }
            img { max-width: 100%; margin: 10px; border: 1px solid #ddd; }
        </style>
    </head>
    <body>
        <h1>当前文件夹图片列表</h1>
        <div>
"""
    
    print(natsorted(images))
    for img in natsorted(images):
        html_content += f'<img src="{img}" alt="{os.path.basename(img)}">\n'
    html_content += "</div></body></html>"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"成功生成HTML文件：{output_file}")
    

def get_images(current_dir, extensions=('jpg', 'png', 'gif', 'bmp')):
    images = []
    for root, _, files in os.walk(current_dir):
        for file in files:
            if file.lower().endswith(extensions):
                # 生成相对于当前目录的路径
                rel_path = os.path.relpath(os.path.join(root, file), current_dir)
                images.append(rel_path.replace('\\', '/'))  # 统一路径分隔符
    return images


def main():
    current_dir = os.getcwd()  # 获取当前文件夹路径
    images = get_images(current_dir)
    if not images:
        print("未找到图片文件！")
        return
    generate_html(images)

if __name__ == "__main__":
    main()