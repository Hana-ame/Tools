#!/usr/bin/env python3
"""
AVIF批量转换脚本
支持将图片（PNG/JPEG等）和MP4视频文件转换为AVIF格式
使用方法：直接将文件或文件夹拖拽到脚本上即可
"""

import os
import sys
import subprocess
import threading
from pathlib import Path
from tkinter import Tk, filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText
import tkinter as tk

class AVIFConverter:
    def __init__(self):
        self.root = Tk()
        self.root.title("AVIF格式转换工具")
        self.root.geometry("800x600")
        
        # 创建界面组件
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 标题
        title_label = ttk.Label(main_frame, text="AVIF格式转换工具", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 参数设置框架
        param_frame = ttk.LabelFrame(main_frame, text="转换参数", padding="10")
        param_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 质量参数
        ttk.Label(param_frame, text="CRF质量 (0-63，值越小质量越高):").grid(row=0, column=0, sticky=tk.W)
        self.crf_var = tk.StringVar(value="23")
        crf_entry = ttk.Entry(param_frame, textvariable=self.crf_var, width=10)
        crf_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # CPU使用参数
        ttk.Label(param_frame, text="CPU使用率 (0-8，值越大速度越快):").grid(row=1, column=0, sticky=tk.W)
        self.cpu_var = tk.StringVar(value="4")
        cpu_entry = ttk.Entry(param_frame, textvariable=self.cpu_var, width=10)
        cpu_entry.grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="选择文件", 
                  command=self.select_files).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="选择文件夹", 
                  command=self.select_folder).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="开始转换", 
                  command=self.start_conversion).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="清空日志", 
                  command=self.clear_log).pack(side=tk.LEFT)
        
        # 进度条
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # 日志输出
        log_frame = ttk.LabelFrame(main_frame, text="转换日志", padding="5")
        log_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.log_text = ScrolledText(log_frame, height=20, width=80)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
    def log_message(self, message):
        """添加日志消息"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def clear_log(self):
        """清空日志"""
        self.log_text.delete(1.0, tk.END)
        
    def select_files(self):
        """选择多个文件"""
        files = filedialog.askopenfilenames(
            title="选择要转换的图片或视频文件",
            filetypes=[("媒体文件", "*.jpg *.jpeg *.png *.bmp *.mp4 *.mov *.avi"), 
                      ("所有文件", "*.*")]
        )
        if files:
            self.files_to_convert = list(files)
            self.log_message(f"已选择 {len(files)} 个文件")
            
    def select_folder(self):
        """选择文件夹"""
        folder = filedialog.askdirectory(title="选择包含媒体文件的文件夹")
        if folder:
            self.files_to_convert = self.find_media_files(folder)
            self.log_message(f"在文件夹中找到 {len(self.files_to_convert)} 个媒体文件")
            
    def find_media_files(self, folder):
        """查找文件夹中的媒体文件"""
        media_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.mp4', '.mov', '.avi'}
        media_files = []
        
        for file_path in Path(folder).rglob('*'):
            if file_path.suffix.lower() in media_extensions:
                media_files.append(str(file_path))
                
        return media_files
    
    def check_ffmpeg(self):
        """检查FFmpeg是否可用"""
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
            
    def convert_to_avif(self, input_file, output_file, crf, cpu_used):
        """使用FFmpeg转换文件为AVIF格式[9,10,11](@ref)"""
        
        # 构建FFmpeg命令
        cmd = [
            'ffmpeg',
            '-i', input_file,
            '-c:v', 'libaom-av1',
            '-crf', str(crf),
            '-cpu-used', str(cpu_used),
            '-still-picture', '1' if not input_file.lower().endswith(('.mp4', '.mov', '.avi')) else '0',
            '-b:v', '0',
            '-y',  # 覆盖输出文件
            output_file
        ]
        
        self.log_message(f"转换: {os.path.basename(input_file)} → {os.path.basename(output_file)}")
        self.log_message(f"命令: {' '.join(cmd)}")
        
        try:
            # 执行转换
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                     stderr=subprocess.STDOUT, 
                                     universal_newlines=True)
            
            # 实时输出进度
            for line in process.stdout:
                if 'time=' in line:
                    time_info = [part for part in line.split() if 'time=' in part]
                    if time_info:
                        self.log_message(f"进度: {time_info[0]}")
            
            process.wait()
            
            if process.returncode == 0:
                self.log_message(f"✓ 转换成功: {os.path.basename(output_file)}")
                return True
            else:
                self.log_message(f"✗ 转换失败: {os.path.basename(input_file)}")
                return False
                
        except Exception as e:
            self.log_message(f"✗ 错误: {str(e)}")
            return False
    
    def start_conversion(self):
        """开始转换过程"""
        if not hasattr(self, 'files_to_convert') or not self.files_to_convert:
            messagebox.showerror("错误", "请先选择要转换的文件或文件夹")
            return
            
        # 检查FFmpeg
        if not self.check_ffmpeg():
            messagebox.showerror("错误", 
                "未找到FFmpeg或版本不支持AV1编码。请确保已安装支持libaom-av1的FFmpeg[13](@ref)")
            return
            
        # 获取参数
        try:
            crf = int(self.crf_var.get())
            cpu_used = int(self.cpu_var.get())
            
            if not (0 <= crf <= 63):
                raise ValueError("CRF值应在0-63范围内")
            if not (0 <= cpu_used <= 8):
                raise ValueError("CPU使用率应在0-8范围内")
                
        except ValueError as e:
            messagebox.showerror("参数错误", f"参数设置错误: {str(e)}")
            return
        
        # 在后台线程中执行转换
        thread = threading.Thread(target=self._conversion_thread, 
                                 args=(crf, cpu_used))
        thread.daemon = True
        thread.start()
        
    def _conversion_thread(self, crf, cpu_used):
        """转换线程"""
        total_files = len(self.files_to_convert)
        success_count = 0
        
        self.progress['maximum'] = total_files
        self.progress['value'] = 0
        
        for i, input_file in enumerate(self.files_to_convert):
            # 生成输出文件名
            input_path = Path(input_file)
            output_file = str(input_path.with_suffix('.avif'))
            
            # 执行转换
            if self.convert_to_avif(input_file, output_file, crf, cpu_used):
                success_count += 1
                
            # 更新进度条
            self.progress['value'] = i + 1
            self.root.update()
        
        # 显示结果摘要
        self.log_message("\n" + "="*50)
        self.log_message(f"转换完成! 成功: {success_count}/{total_files}")
        
        if success_count == total_files:
            messagebox.showinfo("完成", f"所有 {total_files} 个文件转换成功!")
        else:
            messagebox.showwarning("完成", 
                f"转换完成! 成功: {success_count}/{total_files}")

def main():
    """主函数 - 支持命令行拖放操作"""
    if len(sys.argv) > 1:
        # 命令行模式
        converter = AVIFConverter()
        converter.files_to_convert = sys.argv[1:]
        converter.log_message(f"通过拖放接收 {len(converter.files_to_convert)} 个文件")
        
        # 自动开始转换（使用默认参数）
        converter.root.after(100, lambda: converter.start_conversion())
    else:
        # GUI模式
        converter = AVIFConverter()
        
    converter.root.mainloop()

if __name__ == "__main__":
    main()