#!/usr/bin/env python3
"""
FastAPI 测试服务器 - Markdown 代码块执行器（改进版栈解析）
修复：支持同级反引号嵌套（如 python 内嵌 bash），正确保留外层代码块结构。
"""

import os
import subprocess
import re
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
import uvicorn

# ============ 安全配置 ============
ALLOW_UNSAFE = os.getenv("ALLOW_CODE_EXECUTION", "false").lower() == "true"
ALLOW_UNSAFE = True  # 测试时强制开启

app = FastAPI(
    title="Markdown Code Executor API",
    version="4.1.0",
    description="支持嵌套代码块的栈解析器"
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

# ============ 执行器 ============
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

# ============ 改进的栈解析逻辑 ============
def process_markdown(markdown_text: str) -> str:
    lines = markdown_text.splitlines(keepends=False)
    output_lines = []
    stack = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # 预检查：这一行是否是一个带语言的代码块开始标记 (如 ```python, ```bash)
        # 这用于区分是"结束当前块"还是"开始嵌套块"
        start_marker_match = re.match(r'^(\s*)(`{3,})(\w+)\s*$', line)

        # --- 逻辑分支1: 处理代码块结束或嵌套开始 ---
        if stack:
            current_block = stack[-1]
            min_ticks = current_block['backtick_count']
            
            # 检查是否匹配结束标记 (反引号数量 >= 开始时的数量)
            end_match = re.match(rf'^(\s*)(`{{{min_ticks},}})\s*$', line)
            
            if end_match:
                # 【关键修改】如果这一行同时也匹配“带语言的开始标记”，则视为嵌套开始
                if start_marker_match:
                    # 认为是嵌套块开始，压入栈
                    indent = start_marker_match.group(1)
                    backticks = start_marker_match.group(2)
                    lang = start_marker_match.group(3).lower()
                    
                    stack.append({
                        'lang': lang,
                        'indent': indent,
                        'backtick_count': len(backticks),
                        'start_line': line,
                        'content_lines': [],
                        'end_line': None
                    })
                    i += 1
                    continue
                else:
                    # 没有 language 标识，认为是当前块的结束
                    current_block['end_line'] = line
                    closed_block = stack.pop()
                    
                    # 处理闭合的块，返回处理后的文本行
                    processed_lines = _handle_closed_block(closed_block)
                    
                    # 【关键修改】将结果追加到父级内容或最终输出
                    if stack:
                        stack[-1]['content_lines'].extend(processed_lines)
                    else:
                        output_lines.extend(processed_lines)
                    
                    i += 1
                    continue
            else:
                # 不是结束标记，作为内容添加到当前块
                current_block['content_lines'].append(line)
                i += 1
                continue

        # --- 逻辑分支2: 处理顶层代码块开始 ---
        # 如果不在栈中，检查是否为开始标记
        if start_marker_match:
            indent = start_marker_match.group(1)
            backticks = start_marker_match.group(2)
            lang = start_marker_match.group(3).lower()
            stack.append({
                'lang': lang,
                'indent': indent,
                'backtick_count': len(backticks),
                'start_line': line,
                'content_lines': [],
                'end_line': None
            })
            i += 1
            continue

        # --- 逻辑分支3: 普通文本 ---
        # 如果不在任何块中，直接输出
        if not stack:
            output_lines.append(line)
        else:
            # 理论上不应走到这里，上面的逻辑已经处理了块内情况
            stack[-1]['content_lines'].append(line)
        
        i += 1

    # 处理未闭合的块
    while stack:
        unclosed = stack.pop()
        # 将未闭合的内容回填
        if stack:
            stack[-1]['content_lines'].append(unclosed['start_line'])
            stack[-1]['content_lines'].extend(unclosed['content_lines'])
        else:
            output_lines.append(unclosed['start_line'])
            output_lines.extend(unclosed['content_lines'])

    return '\n'.join(output_lines)

def _handle_closed_block(block: Dict[str, Any]) -> List[str]:
    """处理一个完整闭合的代码块，返回处理后的行列表"""
    result_lines = []
    
    lang = block['lang']
    indent = block['indent']
    start_line = block['start_line']
    content_lines = block['content_lines']
    end_line = block['end_line']

    # 1. 原样输出原始代码块（开始行 + 内容 + 结束行）
    result_lines.append(start_line)
    result_lines.extend(content_lines)
    result_lines.append(end_line)

    # 2. 执行代码
    is_bash = lang in ('bash', 'sh', '')
    is_python = lang in ('python', 'py')
    
    if is_bash or is_python:
        # 注意：content_lines 可能已经包含了嵌套块处理后的结果
        code_content = '\n'.join(content_lines).rstrip('\n')
        
        if is_bash:
            res = execute_bash(code_content)
        else:
            res = execute_python(code_content)
        
        # 追加 output 块
        result_lines.append(f"{indent}```output")
        if res:
            for res_line in res.splitlines():
                result_lines.append(f"{indent}{res_line}")
        else:
            result_lines.append(f"{indent}(无输出)")
        result_lines.append(f"{indent}```")

    return result_lines

# ============ 文本处理主函数 ============
def process_text(text: str, operation: str) -> str:
    if operation == "execute_markdown":
        return process_markdown(text)
    # ... 其他操作保持不变 ...
    elif operation == "reverse": return text[::-1]
    elif operation == "uppercase": return text.upper()
    elif operation == "lowercase": return text.lower()
    elif operation == "count":
        return f"行数: {len(text.splitlines())}, 字符数: {len(text)}"
    elif operation == "trim": return text.strip()
    elif operation == "bash":
        # 简单的 bash 测试操作
        if not text.strip().startswith("echo "): return "错误：只允许 echo"
        try:
            return subprocess.run(text, shell=True, capture_output=True, text=True, timeout=2).stdout.strip()
        except: return "执行出错"
    return text

# ============ API 路由 ============
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
    print("🚀 启动服务 (改进版栈解析，支持同符号嵌套)")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")