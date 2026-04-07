#!/usr/bin/env python3
"""
FastAPI 测试服务器 - Markdown 代码块执行器
功能：精确解析 Markdown 代码块（支持内容中的 ```），执行 bash/sh/空 和 python/py 代码块，
      保留原代码块并附加 ```output ... ``` 结果块。
端口：8000
支持 CORS
"""

import os
import subprocess
import re
from typing import List, Tuple, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
import uvicorn

# ============ 安全配置 ============
ALLOW_UNSAFE = os.getenv("ALLOW_CODE_EXECUTION", "false").lower() == "true"

app = FastAPI(
    title="Markdown Code Executor API",
    version="3.0.0",
    description="精确解析代码块并执行，支持内容中的 ``` 符号"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ 数据模型 ============
class TextRequest(BaseModel):
    text: str
    operation: str = "execute_markdown"

    @field_validator('operation')
    @classmethod
    def validate_operation(cls, v):
        allowed = {"reverse", "uppercase", "lowercase", "bash", "count", "trim", "execute_markdown"}
        if v not in allowed:
            raise ValueError(f"不支持的操作: {v}")
        return v

class TextResponse(BaseModel):
    result: str
    operation: str
    original_length: int
    processed_length: int

# ============ 代码块执行器 ============
def execute_bash(code: str) -> str:
    if not ALLOW_UNSAFE:
        allowed = ("echo", "ls", "pwd", "date", "whoami", "cat ")
        if not any(code.strip().startswith(p) for p in allowed):
            return f"[安全限制] 仅允许: {', '.join(allowed)}"
    try:
        result = subprocess.run(
            code, shell=True, capture_output=True, text=True, timeout=5,
            executable="/bin/bash" if os.name != "nt" else None
        )
        return (result.stdout or result.stderr).strip() or "(无输出)"
    except subprocess.TimeoutExpired:
        return "错误：命令执行超时（5秒）"
    except Exception as e:
        return f"执行错误: {str(e)}"

def execute_python(code: str) -> str:
    if not ALLOW_UNSAFE:
        if "print(" not in code and "import" not in code:
            return "[安全限制] 仅允许 print/import"
    try:
        result = subprocess.run(
            ["python", "-c", code], capture_output=True, text=True, timeout=5
        )
        return (result.stdout or result.stderr).strip() or "(无输出)"
    except subprocess.TimeoutExpired:
        return "错误：Python 执行超时（5秒）"
    except Exception as e:
        return f"执行错误: {str(e)}"

# ============ 精确的代码块解析（基于反引号计数） ============
def get_code_blocks(text: str) -> List[Tuple[str, str, str]]:
    """
    返回列表，每个元素为 (language, content, full_block)
    language: 小写语言标识（空字符串表示无标识）
    content: 代码块内容（去除首尾空白行）
    full_block: 完整的原始代码块文本（含开始和结束标记）
    """
    lines = text.splitlines(keepends=True)
    blocks = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        # 匹配代码块开始：可选缩进 + 连续反引号(>=3) + 可选语言标识
        match = re.match(r'^(\s*)(`{3,})(\w*)\s*$', line)
        if match:
            indent = match.group(1)
            backticks = match.group(2)      # 反引号字符串，如 "```"
            lang = match.group(3).lower()
            min_ticks = len(backticks)

            # 收集代码块内容，直到遇到相同或更多数量的反引号
            content_lines = []
            i += 1
            end_line = None
            while i < n:
                cur = lines[i]
                # 检查当前行是否由 可选缩进 + 反引号(>=min_ticks) + 空白 组成
                end_match = re.match(rf'^(\s*)(`{{{min_ticks},}})\s*$', cur)
                if end_match:
                    # 确保反引号数量不少于开始的数量
                    if len(end_match.group(2)) >= min_ticks:
                        end_line = cur
                        i += 1
                        break
                content_lines.append(cur)
                i += 1

            if end_line is None:
                # 未闭合，视为普通文本，回退
                continue

            # 拼接代码块内容，并去掉末尾多余换行
            content = ''.join(content_lines).rstrip('\n')
            # 构造完整原始块
            full_block = line + ''.join(content_lines) + end_line

            blocks.append((lang, content, full_block))
        else:
            i += 1
    return blocks

def process_markdown(markdown_text: str) -> str:
    """
    处理 Markdown：找到所有代码块，对可执行的附加 ```output 结果块。
    替换原块为 原块 + 结果块。
    """
    blocks = get_code_blocks(markdown_text)
    if not blocks:
        return markdown_text

    # 按完整块进行替换（注意：可能存在相同的块文本，故使用顺序替换）
    result_text = markdown_text
    for lang, content, full_block in blocks:
        is_bash = lang in ('bash', 'sh', '')
        is_python = lang in ('python', 'py')
        if not (is_bash or is_python):
            continue

        # 执行并获取结果
        if is_bash:
            output = execute_bash(content)
        else:
            output = execute_python(content)

        # 构建结果块（保持与原始块相同的缩进？这里简单使用相同的开头缩进）
        # 提取原始块的缩进（第一行的前导空格）
        first_line = full_block.splitlines()[0] if full_block else ''
        indent_match = re.match(r'^(\s*)', first_line)
        indent = indent_match.group(1) if indent_match else ''
        result_block = f"{indent}```output\n{output}\n{indent}```\n"

        # 替换：原块 + 结果块
        replacement = full_block + '\n' + result_block
        result_text = result_text.replace(full_block, replacement, 1)  # 只替换第一次出现

    return result_text

# ============ 文本处理主函数 ============
def process_text(text: str, operation: str) -> str:
    if operation == "execute_markdown":
        return process_markdown(text)
    elif operation == "reverse":
        return text[::-1]
    elif operation == "uppercase":
        return text.upper()
    elif operation == "lowercase":
        return text.lower()
    elif operation == "count":
        lines = len(text.splitlines())
        words = len(text.split())
        chars = len(text)
        return f"行数: {lines}, 单词数: {words}, 字符数: {chars}"
    elif operation == "trim":
        return text.strip()
    elif operation == "bash":
        text = text.strip()
        if not text.startswith("echo "):
            return f"错误：只允许 echo 命令"
        try:
            result = subprocess.run(text, shell=True, capture_output=True, text=True, timeout=5)
            return (result.stdout or result.stderr).strip() or "(无输出)"
        except subprocess.TimeoutExpired:
            return "错误：命令超时"
        except Exception as e:
            return f"执行错误: {e}"
    return text

# ============ API 路由 ============
@app.get("/")
async def root():
    return {
        "message": "Markdown Code Executor API",
        "version": "3.0.0",
        "endpoints": {
            "POST /process": "处理 Markdown 文本，执行 bash/sh/空 和 python/py 代码块"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/process", response_model=TextResponse)
async def process_endpoint(request: TextRequest):
    try:
        result = process_text(request.text, request.operation)
        return TextResponse(
            result=result,
            operation=request.operation,
            original_length=len(request.text),
            processed_length=len(result)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {e}")

if __name__ == "__main__":
    print("🚀 启动服务 (支持精确代码块解析)")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")