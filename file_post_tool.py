# 将本地文件夹中的文件上传并post到指定的thread中
import os
import requests
from pathlib import Path
from typing import Iterator

def upload_file_put(file_path, url="https://upload.moonchan.xyz/api/upload"):
    """
    使用 PUT 方法上传文件到指定的 URL

    参数:
        url (str): 目标 URL
        file_path (str): 要上传的本地文件路径

    返回:
        requests.Response: 响应对象
    """
    # try:
    # 以二进制读模式打开文件
    with open(file_path, 'rb') as f:
        # 发送 PUT 请求，将文件内容作为请求体
        response = requests.put(url, data=f)
    # 可选的，检查状态码是否为 2xx
    response.raise_for_status()
    return response
    # except FileNotFoundError:
    #     print(f"错误：文件 '{file_path}' 未找到。")
    #     return None
    # except requests.exceptions.RequestException as e:
    #     print(f"请求发生错误: {e}")
    #     return None

def post_to_thread(tid, txt="", p=""):
    """
    向指定线程发送帖子
    
    参数:
    tid: 线程ID
    txt: 帖子文本内容 (可选)
    p: 图片或其他附件参数 (可选)
    
    返回:
    response: 请求响应对象
    """
    endpoint = f"https://moonchan.xyz/api/v2/?bid=0&tid={tid}"
    auth = "DY4X5IHR%7C551e446ae9942a675b7152eb98a1609928c8f5bb4c724a62cdf51eaa8a4c6040"
    
    # 构建请求数据
    payload = {
        "id": "",
        "no": 0,
        "n": "",
        "t": "",
        "txt": txt,
        "p": p
    }
    
    # 设置Cookie - 将认证信息放入Cookie中[1,17](@ref)
    cookies = {
        "auth": auth
    }
    
    try:
        # 发送POST请求
        response = requests.post(
            endpoint,
            json=payload,  # 使用json参数自动序列化并设置Content-Type
            cookies=cookies
        )
        
        # 检查请求是否成功
        response.raise_for_status()
        
        return response
        
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None
    
def get_filename(path):
    """
    从路径中提取文件名（包括扩展名）
    
    参数:
        path (str): 文件路径字符串
    
    返回:
        str: 文件名
    """
    return os.path.basename(path)

def file_iterator(directory_path: str) -> Iterator[str]:
    """
    迭代器：递归遍历目录及其所有子目录，生成每个文件的完整路径

    参数:
        directory_path (str): 要遍历的根目录路径

    返回:
        Iterator[str]: 生成文件完整路径的迭代器

    异常:
        可能会抛出 PermissionError 或 FileNotFoundError，建议调用时处理。
    """
    # 首先检查目录是否存在
    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"目录 '{directory_path}' 不存在")
    if not os.path.isdir(directory_path):
        raise NotADirectoryError(f"'{directory_path}' 不是一个有效的目录")

    # 使用 os.walk 递归遍历
    for root_dir, sub_dirs, files in os.walk(directory_path):
        for file in files:
            # 使用 os.path.join 拼接完整的文件路径
            full_file_path = os.path.join(root_dir, file)
            yield full_file_path

flag = True


for fn in file_iterator("/mnt/c/Users/lumin/Downloads/爱慕 (@im86617687)"):
    # break
    if "1787133881147089342_p0.mp4" in fn: flag = False
    if flag: continue
    tid = 155803
    print(fn)
    resp = upload_file_put(fn)
    print(resp.json())
    url = f"https://upload.moonchan.xyz/api/{resp.json().get("id")}/{get_filename(fn)}"
    post_to_thread(tid,p=url)
    

for fn in file_iterator("/mnt/c/Users/lumin/Downloads/黑猫 (@xiaoAimu_)1"):
    break
    if "1845866965627543874_p1" in fn: flag = False
    if flag: continue
    tid = 155804
    print(fn)
    resp = upload_file_put(fn)
    print(resp.json())
    url = f"https://upload.moonchan.xyz/api/{resp.json().get("id")}/{get_filename(fn)}"
    post_to_thread(tid,p=url)
    

if __name__ != "__main__":
    # # 示例用法
    # thread_id = "155652"  # 替换为实际的线程ID
    # text_content = "这是一个测试帖子"
    # response = post_to_thread(thread_id, txt=text_content)
    
    # if response:
    #     print("帖子发送成功:")
    # else:
    #     print("帖子发送失败")
    pass