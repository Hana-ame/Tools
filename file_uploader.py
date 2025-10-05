import os
import mimetypes
import requests

class ImageUploader:
    """
    图床上传工具类，使用统一的 Session 管理所有请求
    """
    
    def __init__(self):
        """
        初始化上传器，创建共享的 Session 对象
        """
        self.session = requests.Session()
        # 可以在这里设置统一的请求头
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def __del__(self):
        """
        析构函数，确保 Session 被正确关闭
        """
        self.session.close()
        
    @staticmethod
    def get_filename(path: str):
        """
        从路径中提取文件名（包括扩展名）
        
        参数:
            path (str): 文件路径字符串
        
        返回:
            str: 文件名
        """
        return os.path.basename(path)
    
    def upload_moonchan_xyz(self, fn) -> str:
        """
        上传到 moonchan.xyz 图床
        
        参数:
            fn (str): 文件路径
        
        返回:
            str: 上传成功后的文件 URL
        """
        with open(fn, 'rb') as f:
            response = self.session.put("https://upload.moonchan.xyz/api/upload", data=f)
        response.raise_for_status()
        return f'https://upload.moonchan.xyz/api/{response.json().get("id")}/{ImageUploader.get_filename(fn)}'
    
    def img_xxxh_de(self, fn):
        """
        上传到 img.xxxh.de 图床
        
        参数:
            fn (str): 文件路径
        
        返回:
            str: 上传成功后的文件 URL
        """
        mime_type, _ = mimetypes.guess_type(fn)
        with open(fn, 'rb') as f:
            files = {
                'file': (
                    ImageUploader.get_filename(fn),
                    f,
                    mime_type or "application/octet-stream",
                )
            }
            response = self.session.post("https://img.xxxh.de/upload", files=files)
        response.raise_for_status()
        return response.json().get("data")
    
    # pass, but auth-token manually
    def i_111666_best(self, fn):
        """
        上传到 i.111666.best 图床 (需要 auth-token)
        
        参数:
            fn (str): 文件路径
        
        返回:
            str: 上传成功后的文件 URL
        """
        headers = {
            'auth-token': "TB8iIvrVGvHc38CohZLzSnSF9tSrGkUA"  # 请替换为您自己的 token
        }
        mime_type, _ = mimetypes.guess_type(fn)
        with open(fn, 'rb') as f:
            files = {
                'abc': (
                    ImageUploader.get_filename(fn),
                    f,
                    mime_type or "application/octet-stream",
                )
            }
            response = self.session.post("https://i.111666.best/image", files=files, headers=headers)
        response.raise_for_status()
        return f"https://i.111666.best{response.json().get('src')}"
    
    # 用不了, 403错误
    def skyimg_net(self, fn):
        """
        上传到 skyimg.net 图床
        
        参数:
            fn (str): 文件路径
        
        返回:
            str: 上传成功后的文件 URL
        """
        # 首先获取 CSRF token，使用同一个 session 会自动保持 cookie
        headers = {
            "x-csrf-token" : self.session.get("https://skyimg.net/csrf-token").json().get("csrfToken")
        }
        
        mime_type, _ = mimetypes.guess_type(fn)
        with open(fn, 'rb') as f:
            files = {
                'file': (
                    ImageUploader.get_filename(fn),
                    f,
                    mime_type or "application/octet-stream",
                )
            }
            response = self.session.post("https://skyimg.net/upload", files=files, headers=headers)
        response.raise_for_status()
        return response.json()[0].get("url")
    
    # 用不了, 403错误
    def skyimg_net_webp(self, fn):
        """
        上传到 skyimg.net 图床并转换为 WebP 格式
        
        参数:
            fn (str): 文件路径
        
        返回:
            str: 上传成功后的文件 URL
        """
        # 首先获取 CSRF token，使用同一个 session 会自动保持 cookie
        headers = {
            "x-csrf-token" : self.session.get("https://skyimg.net/csrf-token").json().get("csrfToken")
        }
        
        mime_type, _ = mimetypes.guess_type(fn)
        with open(fn, 'rb') as f:
            files = {
                'file': (
                    ImageUploader.get_filename(fn),
                    f,
                    mime_type or "application/octet-stream",
                )
            }
            response = self.session.post("https://skyimg.net/upload?webp=true", files=files, headers=headers)
        response.raise_for_status()
        return response.json()[0].get("url")
    
    def cdn_violet_vin(self, fn):
        """
        上传到 cdn.violet.vin 图床
        
        参数:
            fn (str): 文件路径
        
        返回:
            str: 上传成功后的文件 URL
        """
        mime_type, _ = mimetypes.guess_type(fn)
        with open(fn, 'rb') as f:
            files = {
                'file': (
                    ImageUploader.get_filename(fn),
                    f,
                    mime_type or "application/octet-stream",
                )
            }
            response = self.session.post("https://cdn.violet.vin/upload", files=files)
        response.raise_for_status()
        return f"https://cdn.violet.vin/v2/{response.json().get("data").get("id")}.jpeg"
    
    def close(self):
        """
        手动关闭 Session 连接
        """
        self.session.close()

# 使用示例
if __name__ == '__main__':
    # 创建上传器实例
    uploader = ImageUploader()
    
    try:
        # 使用不同的方法上传到不同图床
        url1 = uploader.skyimg_net_webp("./archive/3155086-3.png")
        print(f"Skyimg.net WebP URL: {url1}")
        
        # 可以继续使用同一个 uploader 实例上传到其他图床
        # url2 = uploader.upload_moonchan_xyz("./archive/3155086-3.png")
        # print(f"Moonchan URL: {url2}")
        
    finally:
        # 确保连接被关闭
        uploader.close()