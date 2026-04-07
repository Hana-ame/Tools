#!/usr/bin/env python3
"""
FastAPI 测试服务器 - Markdown 代码块执行器（临时文件执行版）
功能：使用栈状态机精确解析代码块，支持内容中的 ``` 嵌套。
      Python 执行改为创建临时文件运行，避免 -c 模式下的转义问题。
"""

import os
import subprocess
import re
import tempfile
import sys
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
    version="4.2.0",
    description="栈方式解析，支持嵌套，Python采用临时文件执行"
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
    
    temp_file_path = None
    try:
        # 创建临时文件，delete=False 以便子进程读取
        # 使用 utf-8 编码写入
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(code)
            temp_file_path = f.name
        
        # 使用当前 Python 解释器执行，确保环境一致
        result = subprocess.run(
            [sys.executable, temp_file_path], 
            capture_output=True, 
            text=True, 
            timeout=10,
            encoding='utf-8' # 强制使用 utf-8 解码输出
        )
        
        # 优先返回标准输出，其次标准错误
        output = result.stdout.strip() if result.stdout else ""
        error = result.stderr.strip() if result.stderr else ""
        
        if error:
            # 尝试美化错误输出，去除临时文件路径信息
            error = error.replace(temp_file_path, "<string>")
            return f"错误：\n{error}"
        
        return output or "(无输出)"
        
    except subprocess.TimeoutExpired:
        return "错误：Python 执行超时（10秒）"
    except Exception as e:
        return f"执行错误: {str(e)}"
    finally:
        # 清理临时文件
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except Exception:
                pass

# ============ 改进的栈解析逻辑 ============
def process_markdown(markdown_text: str) -> str:
    lines = markdown_text.splitlines(keepends=False)
    output_lines = []
    stack = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # 预检查：这一行是否是一个带语言的代码块开始标记 (如 ```python, ```bash)
        # 注意：必须在行首（允许缩进）且包含语言标识
        start_marker_match = re.match(r'^(\s*)(`{3,})(\w+)\s*$', line)

        # --- 逻辑分支1: 处理代码块结束或嵌套开始 ---
        if stack:
            current_block = stack[-1]
            min_ticks = current_block['backtick_count']
            
            # 检查是否匹配结束标记 (反引号数量 >= 开始时的数量，且无语言标识)
            # 结束标记通常是 ``` 或者更多反引号，且后面没有跟语言（有些方言允许跟空格，这里简化处理）
            end_match = re.match(rf'^(\s*)(`{{{min_ticks},}})\s*$', line)
            
            if end_match:
                # 【关键逻辑】如果同时匹配开始标记（带语言），视为嵌套开始
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
                else:
                    # 否则视为结束当前块
                    current_block['end_line'] = line
                    closed_block = stack.pop()
                    
                    # 处理闭合的块
                    processed_lines = _handle_closed_block(closed_block)
                    
                    # 将结果追加到父级内容或最终输出
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
        if not stack:
            output_lines.append(line)
        else:
            # 理论上不应走到这里，上面的逻辑已经处理了块内情况
            stack[-1]['content_lines'].append(line)
        
        i += 1

    # 处理未闭合的块
    while stack:
        unclosed = stack.pop()
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
    
    # 注意：如果内容中包含了嵌套块处理后的结果，这里的 code_content 会包含嵌套块的输出
    # 这是符合预期的，因为我们要把整个块当作代码执行
    if is_bash or is_python:
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
    elif operation == "reverse": return text[::-1]
    elif operation == "uppercase": return text.upper()
    elif operation == "lowercase": return text.lower()
    elif operation == "count":
        return f"行数: {len(text.splitlines())}, 字符数: {len(text)}"
    elif operation == "trim": return text.strip()
    elif operation == "bash":
        if not ALLOW_UNSAFE: return "[安全限制]"
        try:
            return subprocess.run(text, shell=True, capture_output=True, text=True, timeout=2).stdout.strip()
        except: return "执行出错"
    return text

# ============ API 路由 ============
@app.get("/")
async def root():
    return {
        "message": "Markdown Code Executor API (Stack Parser)",
        "version": "4.2.0",
        "endpoints": {"POST /process": "处理 Markdown 文本"}
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
    print("🚀 启动服务 (栈方式解析，支持嵌套，临时文件执行)")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")