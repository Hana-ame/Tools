# main file

from utils import *
from page import *
import json
from compile_markdown_to_html import compile_markdown_to_html

def save_to_json(metadata_list: List[FileMetadata], json_file: str):
    """将文件元数据保存到JSON文件"""
    with open(json_file, 'w') as f:
        json.dump([metadata.to_dict() for metadata in metadata_list], f, indent=4)

def load_from_json(json_file: str) -> List[FileMetadata]:
    """从JSON文件加载文件元数据"""
    with open(json_file, 'r') as f:
        data = json.load(f)
        return [FileMetadata(**item) for item in data]

def get_folders(config: dict) -> list:
    """从配置中获取文件夹和标签列表"""
    return config.get("directories", [])
def get_tags(config: dict) -> list:
    """从配置中获取在显示在头的标签列表"""
    return config.get("tags", [])
    

def main():
    """主函数"""
    config = read_config("blog.yaml")
    folders = get_folders(config)
    tags = get_tags(config)
    all_metadata: List[FileMetadata] = []

    for folder in folders:
        dir_path = folder['dir']
        tags = folder['tags']
        metadata = process_files_in_directory(dir_path, tags)
        all_metadata.extend(metadata)

    # 在生成 HTML 之前对 metadata_list 按创建时间降序排序
    all_metadata.sort(key=lambda x: x.create_date, reverse=True)

    # 保存到JSON文件
    json_file_path = "file_metadata.json"
    save_to_json(all_metadata, json_file_path)
    print(f"文件元数据已保存到 {json_file_path}")

    # 从JSON文件加载
    loaded_metadata = load_from_json(json_file_path)
    print("从JSON文件加载的元数据：")
    for metadata in loaded_metadata:
        print(metadata)

    dist_path = config['dist']
    for metadata in all_metadata:
        title = metadata.title
        md_file_path = metadata.filepath
        output_html_path = os.path.join(dist_path,"article" ,f"{metadata.sha1sum}.html")
        # convert_md_to_html(title, md_file_path, output_html_path)
        compile_markdown_to_html(title, md_file_path, output_html_path)

    
    generate_index([], all_metadata, os.path.join(dist_path, "index.html"))


if __name__ == "__main__":
    main()
    
    # 使用示例
    # md_file_path = 'example.md'  # 输入 Markdown 文件路径
    # output_html_path = 'output.html'  # 输出 HTML 文件路径
    # convert_md_to_html(md_file_path, output_html_path)

#end