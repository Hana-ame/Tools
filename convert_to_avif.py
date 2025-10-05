# convert 

# return {
#     'file': str(file_path),
#     'status': 'success',
#     'message': f'处理完成: {file_path.name}',
#     'output': f'{file_path.stem}_processed{file_path.suffix}'
# }
from dataclasses import dataclass, asdict, field
from enum import Enum
from typing import Optional, Union
from pathlib import Path

import os
import subprocess


class StatusCode(Enum):
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    PENDING = "pending"

@dataclass
class ReturnType:
    """用于表示操作返回结果的数据类"""
    
    file: str
    # status: Union[str, bool]  # 可以是字符串或布尔值
    status: StatusCode
    message: str
    output: str = ""  # 默认值为空字符串
    
    def to_dict(self) -> dict:
        """将对象转换为字典[1,3](@ref)
        
        Returns:
            dict: 包含所有属性的字典
        """
        """增强的字典转换，处理枚举类型[3](@ref)"""
        result = asdict(self)
        result['status'] = self.status.value  # 将枚举转换为值
        return result
    
    def is_successful(self) -> bool:
        """检查操作是否成功[8](@ref)"""
        if isinstance(self.status, bool):
            return self.status
        # return self.status.lower() in ('success', 'true', 'ok', '完成')
        return self.status == StatusCode.SUCCESS
    
    def __str__(self) -> str:
        """返回对象的字符串表示[2](@ref)"""
        return f"ReturnType(file={self.file}, status={self.status}, message={self.message})"
    
    @classmethod
    def create_success(cls, file_path: Union[str, Path], message: str = "", output: str = "") -> 'ReturnType':
        """创建成功结果的快捷方法"""
        file_str = str(file_path)
        if not message:
            message = f'处理完成: {Path(file_path).name}'
        if not output:
            output = f'{Path(file_path).stem}_processed{Path(file_path).suffix}'
        
        # return cls(file=file_str, status='success', message=message, output=output)
        return cls(file=file_str, status=StatusCode.SUCCESS, message=message, output=output)
    
    @classmethod
    def create_error(cls, file_path: Union[str, Path], error_message: str) -> 'ReturnType':
        """创建错误结果的快捷方法"""
        # return cls(file=str(file_path), status='error', message=error_message, output="")
        return cls(file=str(file_path), status=StatusCode.ERROR, message=error_message, output="")

def process_file(file_path: str) -> ReturnType:
    """
    将媒体文件转换为 AVIF 格式
    
    Args:
        file_path: 输入文件的完整路径
        
    Returns:
        ReturnType: 包含处理结果的对象
    """
    print(file_path)
    
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            return ReturnType(
                file=file_path,
                status=StatusCode.ERROR,
                message=f'文件不存在: {file_path}',
                output=''
            )
        
        # 使用 pathlib 处理路径
        input_path = Path(file_path)
        
        # 生成输出文件名：源文件名 + .avif
        output_filename = f"{input_path.stem}.avif"
        output_path = input_path.parent / output_filename
        
        # 构建 FFmpeg 命令
        # 使用 libaom-av1 编码器进行 AVIF 转换
        command = [
            'ffmpeg',
            '-i', str(input_path),      # 输入文件
            '-c:v', 'libaom-av1',       # 视频编码器
            '-still-picture', '1',      # 静态图片模式（适合 AVIF）
            '-crf', '30',               # 质量参数（0-63，值越小质量越高）
            '-pix_fmt', 'yuv420p',      # 像素格式
            str(output_path)            # 输出文件
        ]
        
        # 执行 FFmpeg 命令[1,6](@ref)
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True  # 如果命令失败则抛出异常
        )
        
        # 检查输出文件是否生成成功
        if output_path.exists():
            return ReturnType(
                file=str(input_path),
                status=StatusCode.SUCCESS,
                message=f'成功转换: {input_path.name} -> {output_filename}',
                output=str(output_path)
            )
        else:
            return ReturnType(
                file=str(input_path),
                status=StatusCode.ERROR,
                message='转换完成但输出文件未生成',
                output=''
            )
            
    except subprocess.CalledProcessError as e:
        # FFmpeg 命令执行失败
        error_msg = f"FFmpeg 转换失败: {e.stderr.strip() if e.stderr else str(e)}"
        return ReturnType(
            file=file_path,
            status=StatusCode.ERROR,
            message=error_msg,
            output=''
        )
        
    except FileNotFoundError:
        # FFmpeg 未安装
        return ReturnType(
            file=file_path,
            status=StatusCode.ERROR,
            message='FFmpeg 未安装或未在系统路径中找到',
            output=''
        )
        
    except Exception as e:
        # 其他异常
        return ReturnType(
            file=file_path,
            status=StatusCode.ERROR,
            message=f'处理过程中发生错误: {str(e)}',
            output=''
        )
