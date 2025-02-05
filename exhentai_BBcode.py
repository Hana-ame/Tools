import re
import sys
import hashlib
import requests
from lxml import html
from lxml import etree
import pyperclip

def copy_text_to_clipboard(text):
     """将文本复制到剪贴板。

     Args:
         text: 要复制的文本字符串。
     """
     try:
        pyperclip.copy(text)
        print(f"Text copied to clipboard: {text}")
        return True
     except pyperclip.PyperclipException as e:
        print(f"Error copying to clipboard, Please make sure you have installed the required dependencies: {e}")
        return False

def get(url):
    return requests.get(url, headers={"Cookie":"pass=pass"})

# 从gallery url到bbcode

def get_all_hrefs(url):
    """
    访问指定 URL 的网页，并使用 XPath 提取所有 <a> 标签的 href 属性。

    Args:
        url (str): 要访问的网页 URL。

    Returns:
        list: 一个包含所有 href 值的列表。如果出现错误，返回 None。
    """
    print(url, "...")
    try:
        response = get(url)
        response.raise_for_status()  # 检查 HTTP 错误
        response.encoding = response.apparent_encoding # 防止中文乱码

        tree = html.fromstring(response.text)
        hrefs = tree.xpath('//a/@href')
        return hrefs
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching URL: {e}")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")

def get_max_p_value(urls):
    p_values = []
    for url in urls:
        if url.startswith("/g/"):
            # 找到 p= 的位置并提取值
            p_param = url.split("p=")
            if len(p_param) > 1:
                p_value = int(p_param[1])  # 转换为整数
                p_values.append(p_value)

    # 找到最大的 p 值
    max_p_value = max(p_values) if p_values else 0
    return max_p_value+1

def extract_url_params(url):
    """
    从给定的 URL 中提取数字和十六进制字符串参数。

    Args:
      url: 需要提取参数的 URL 字符串。

    Returns:
      一个元组，包含提取的数字部分和十六进制字符串部分，如果未找到匹配项则返回 (None, None)。
    """
    match = re.search(r'/g/(\d+)/([a-f0-9]+)', url)
    if match:
        number_part = match.group(1)
        hex_part = match.group(2)
        return number_part, hex_part
    else:
        raise Exception(f"{url} 没有需要的key和id")

def construct_url(id, key, page=0):
    """
    使用给定的 ID 和 Key 构建 URL。

    Args:
      id_str: URL 中的 ID 部分 (字符串)。
      key_str: URL 中的 Key 部分 (字符串)。

    Returns:
      构建好的 URL 字符串。
    """
    url = f"https://ex.moonchan.xyz/g/{id}/{key}/?p={page}"
    return url


def generate_bbcode_from_url(target_url):
    """
     给定一个包含图片链接的 /g/ URL，返回一个包含图片链接的 BBCode 字符串。
     Args:
         target_url: 需要解析的网页 URL，形如 https://ex.moonchan.xyz/g/3184765/ef6245cf4e/

     Returns:
         一个包含图片链接的 BBCode 字符串。
    """
    all_links = get_all_hrefs(target_url)
    max_p_value = get_max_p_value(all_links)

    id, key = extract_url_params(target_url)

    if not id or not key:
        raise Exception(f"Error: Could not extract ID and Key from url: {target_url}")

    links_arr_arr = []
    for p in range(max_p_value):
        page_url = construct_url(id, key, str(p))
        links_arr = get_all_hrefs(page_url)
        # 过滤 /s/ 开头的链接
        filted_links_arr = list(filter(lambda url: url.startswith("/s/"), links_arr))
        links_arr_arr.append(filted_links_arr)

    BBCode = ""
    for links_arr in links_arr_arr:
        for link in links_arr:
            BBCode += "[img]" + "https://ex.moonchan.xyz" + link + "?redirect_to=image" + "[/img]" + "\n"
    
    return BBCode


# 图片到sha1sum

def get_image_sha1(image_url):
    """
    从图片 URL 获取图片的 SHA1 校验和。

    Args:
      image_url: 图片的 URL 字符串。

    Returns:
      图片的 SHA1 校验和（十六进制字符串），如果发生错误则返回 None。
    """
    try:
        response = requests.get(image_url, stream=True) # 使用stream=True， 避免下载整个图片到内存
        response.raise_for_status() # 检查是否成功获取图片

        sha1_hash = hashlib.sha1()

        # 分块读取图像数据，避免大文件占用过多内存
        for chunk in response.iter_content(chunk_size=4096):
          sha1_hash.update(chunk)

        return sha1_hash.hexdigest()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching image from URL: {image_url}, Error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def get_g_links_from_hash(image_url):
    """
    获取图片的 SHA1 校验和，访问相应 URL 并使用 XPath 获取 /g/ 开头的链接。

    Args:
      image_url: 图片的 URL 字符串。

    Returns:
      一个包含所有 /g/ 开头链接的列表，如果发生错误则返回空列表。
    """
    sha1_hash = get_image_sha1(image_url)
    if not sha1_hash:
        return []

    print(f"sha1 = {sha1_hash}")

    hash_url = f"https://ex.moonchan.xyz/?f_shash={sha1_hash}"
    try:
        response = get(hash_url)
        response.raise_for_status()
        html_content = response.text
        tree = etree.HTML(html_content)

        # 使用 XPath 获取 /g/ 开头的链接
        links = tree.xpath('//a[starts-with(@href, "/g/")]/@href')

        # 确保返回的链接都是绝对路径
        absolute_links = [f"https://ex.moonchan.xyz{link}" for link in links]
        return absolute_links
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching URL with hash: {hash_url}, Error: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")


# if __name__ == "__main__":
#     target_url = sys.argv[1] if len(sys.argv) > 1 else "https://ex.moonchan.xyz/g/3184765/ef6245cf4e/"
    
#     bbcode = generate_bbcode_from_url(target_url)

#     if bbcode:
#         print(bbcode)
#     else:
#         print("Failed to generate BBCode.")

def generate_bbcode_from_hash(image_url):
    l = get_g_links_from_hash(image_url)
    if len(l) > 0:
        return generate_bbcode_from_url(l[0])
    raise Exception("通过图片sha1值寻找失败，可能是图床压缩过图片或者在ehentai被删除。可尝试在ehentai搜索。")


def get_first_img_src(html_content):
    """
    从 HTML 内容中获取 id="read_tpc" 的元素中第一个 img 元素的 src 属性值。

    Args:
      html_content: 包含 HTML 内容的字符串。

    Returns:
      如果找到，返回第一个 img 元素的 src 属性值，否则返回 None。
    """
    try:
        tree = etree.HTML(html_content)
        xpath_expression = '//*[@id="read_tpc"]//img[1]/@src'
        # 或者使用严格的 xpath
        # xpath_expression = '//*[@id="read_tpc"]/img[1]/@src'
        result = tree.xpath(xpath_expression)
        if result:
            return result[0]
        else:
            return None 
    except Exception as e:
        raise Exception(f"An error occurred: {e}")
    

# if __name__ == '__main__':
#     image_url = "https://p.sda1.dev/21/fe269720a00d6042c4b2d09305d3d14c/3_1.jpg"  # 请替换为你的图片URL
#     # sha1 = get_image_sha1(image_url)
#     bbcode = generate_bbcode_from_hash(image_url)
#     print("bbcode")
#     print(bbcode)
if __name__ == '__main__':
    debug = False
    exurl = "https://ex.moonchan.xyz/g/3214257/e289a12759/"
    if debug and exurl:
        bbcode = (generate_bbcode_from_url(exurl))        
        print(bbcode)
        copy_text_to_clipboard(f"提供在线观看挣点外快 [s:701] \n[sell=1]\n{bbcode}\n[/sell]")
        
    try:
        bbcode = generate_bbcode_from_hash(sys.argv[-1])
        print(bbcode)
        copy_text_to_clipboard(f"提供在线观看挣点外快 [s:701] \n[sell=1]\n{bbcode}\n[/sell]")
    except Exception as e:
        print(e)
        bbcode = (generate_bbcode_from_url(sys.argv[-1]))        
        print(bbcode)
        copy_text_to_clipboard(f"提供在线观看挣点外快 [s:701] \n[sell=1]\n{bbcode}\n[/sell]")