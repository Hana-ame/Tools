#!/usr/bin/env python3
"""
WSL拖放文件并行处理模板
功能：支持拖放多个文件/文件夹，自动递归扫描，并行处理
使用方法：直接将文件或文件夹拖拽到脚本上运行
"""

import sys
import os
import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Callable
import time

# 从这里导入你的实际处理函数
from convert_to_avif import process_file as actual_processor

def process_file(file_path_str: str) -> dict:
    """
    示例处理函数 - 请替换为你的实际处理逻辑
    返回字典包含处理结果和状态信息
    """
    try:
        file_path = Path(file_path_str)
        print(f"处理中: {file_path.name}")
        
        # 这里是你的实际处理逻辑
        # 示例：模拟处理时间
        time.sleep(1)
        
        # 返回处理结果
        return {
            'file': str(file_path),
            'status': 'success',
            'message': f'处理完成: {file_path.name}',
            'output': f'{file_path.stem}_processed{file_path.suffix}'
        }
    except Exception as e:
        return {
            'file': str(file_path_str),
            'status': 'error',
            'message': f'错误: {str(e)}',
            'output': None
        }

def scan_files(paths: List[str], supported_extensions: None | List[str] = None) -> List[str]:
    """
    扫描文件路径，支持文件和文件夹递归扫描[6,8](@ref)
    
    Args:
        paths: 输入路径列表
        supported_extensions: 支持的文件扩展名列表，None表示所有文件
    
    Returns:
        文件路径列表
    """
    file_list = []
    
    for path in paths:
        path_obj = Path(path)
        
        if path_obj.is_file():
            # 单个文件
            if supported_extensions is None or path_obj.suffix.lower() in supported_extensions:
                file_list.append(str(path_obj.resolve()))
        elif path_obj.is_dir():
            # 文件夹递归扫描
            for file_path in path_obj.rglob('*'):
                if file_path.is_file():
                    if supported_extensions is None or file_path.suffix.lower() in supported_extensions:
                        file_list.append(str(file_path.resolve()))
        else:
            print(f"警告: 路径不存在 {path}")
    
    return file_list

def parallel_process_files(file_paths: List[str], 
                         processor_func: Callable, 
                         max_workers: None | int = None,
                         show_progress: bool = True) -> List[dict]:
    """
    并行处理文件列表[9,10](@ref)
    
    Args:
        file_paths: 文件路径列表
        processor_func: 处理函数
        max_workers: 最大线程数，None为自动检测
        show_progress: 是否显示进度
    
    Returns:
        处理结果列表
    """
    if not file_paths:
        return []
    
    results = []
    completed = 0
    total = len(file_paths)
    
    print(f"开始并行处理 {total} 个文件...")
    print(f"使用线程数: {max_workers or '自动'}")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务
        future_to_file = {executor.submit(processor_func, file_path): file_path 
                         for file_path in file_paths}
        
        # 处理完成的任务
        for future in as_completed(future_to_file):
            completed += 1
            file_path = future_to_file[future]
            
            try:
                result = future.result()
                results.append(result)
                
                if show_progress:
                    status_icon = "✓" if result['status'] == 'success' else "✗"
                    print(f"[{completed}/{total}] {status_icon} {result['message']}")
                    
            except Exception as e:
                error_result = {
                    'file': file_path,
                    'status': 'error',
                    'message': f'执行异常: {str(e)}',
                    'output': None
                }
                results.append(error_result)
                print(f"[{completed}/{total}] ✗ 异常: {file_path} - {str(e)}")
    
    return results

def print_summary(results: List[dict]):
    """打印处理摘要"""
    success_count = sum(1 for r in results if r['status'] == 'success')
    error_count = sum(1 for r in results if r['status'] == 'error')
    
    print("\n" + "="*50)
    print("处理摘要:")
    print(f"✓ 成功: {success_count} 个文件")
    print(f"✗ 失败: {error_count} 个文件")
    
    if error_count > 0:
        print("\n失败文件列表:")
        for result in results:
            if result['status'] == 'error':
                print(f"  - {result['file']}: {result['message']}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='拖放文件并行处理器')
    parser.add_argument('paths', nargs='*', help='拖放的文件或文件夹路径')
    parser.add_argument('--ext', nargs='+', help='支持的文件扩展名，如 .jpg .png')
    parser.add_argument('--workers', type=int, help='线程数', default=None)
    parser.add_argument('--no-progress', action='store_true', help='不显示进度')
    
    # 解析命令行参数[6,8](@ref)
    if len(sys.argv) > 1:
        args = parser.parse_args()
    else:
        # 如果没有参数，显示使用说明
        parser.print_help()
        print("\n等待拖放文件...")
        return
    
    # 获取文件列表
    supported_extensions = [ext.lower() if ext.startswith('.') else f'.{ext.lower()}' 
                           for ext in (args.ext or [])]
    
    file_paths = scan_files(args.paths, supported_extensions if args.ext else None)
    
    if not file_paths:
        print("未找到可处理的文件")
        return
    
    print(f"找到 {len(file_paths)} 个文件进行处理")
    
    # 并行处理
    start_time = time.time()
    results = parallel_process_files(
        file_paths, 
        actual_processor,  # 替换为你的处理函数
        # process_file,  # 替换为你的处理函数
        max_workers=args.workers,
        show_progress=not args.no_progress
    )
    end_time = time.time()
    
    # 显示摘要
    print_summary(results)
    print(f"总耗时: {end_time - start_time:.2f} 秒")

if __name__ == "__main__":
    main()