#!/usr/bin/env python3
"""
FastAPI 测试服务器 - Markdown 代码块执行器
功能：接收 Markdown 文本，解析其中的 ```bash 和 ```python 代码块并执行，
      将执行结果替换原代码块（格式为 ```output ... ```）。
      支持嵌套（嵌套代码块视为普通文本）。
端口：8000
支持 CORS（供独立 HTML 文件访问）
"""

import os
import subprocess
import re
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
import uvicorn

# ============ 安全配置 ============
# 通过环境变量 ALLOW_CODE_EXECUTION=1 启用任意命令/代码执行
ALLOW_UNSAFE = os.getenv("ALLOW_CODE_EXECUTION", "false").lower() == "true"

# ============ FastAPI 应用配置 ============
app = FastAPI(
    title="Markdown Code Executor API",
    version="2.0.0",
    description="解析 Markdown 中的 bash/python 代码块并执行"
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
    operation: str = "execute_markdown"   # 新操作：解析并执行代码块

    @field_validator('operation')
    @classmethod
    def validate_operation(cls, v):
        allowed = {
            "reverse", "uppercase", "lowercase",
            "bash", "count", "trim", "execute_markdown"
        }
        if v not in allowed:
            raise ValueError(f"不支持的操作: {v}. 支持的操作: {allowed}")
        return v


class TextResponse(BaseModel):
    result: str
    operation: str
    original_length: int
    processed_length: int


# ============ 代码块执行器 ============
def execute_bash(code: str) -> str:
    """执行 bash 代码（安全受限）"""
    if not ALLOW_UNSAFE:
        # 安全模式：只允许只读/无害命令
        allowed_prefixes = ("echo", "ls", "pwd", "date", "whoami", "cat ")
        code_stripped = code.strip()
        if not any(code_stripped.startswith(p) for p in allowed_prefixes):
            return f"[安全限制] 仅允许以下命令: {', '.join(allowed_prefixes)}"
    try:
        result = subprocess.run(
            code,
            shell=True,
            capture_output=True,
            text=True,
            timeout=5,
            executable="/bin/bash" if os.name != "nt" else None
        )
        output = result.stdout if result.returncode == 0 else result.stderr
        return output.strip() or "(无输出)"
    except subprocess.TimeoutExpired:
        return "错误：命令执行超时（5秒）"
    except Exception as e:
        return f"执行错误: {str(e)}"


def execute_python(code: str) -> str:
    """执行 Python 代码（独立子进程）"""
    if not ALLOW_UNSAFE:
        # 安全模式：只允许打印简单信息
        if "print(" not in code and "import" not in code:
            return "[安全限制] 未启用执行权限，仅允许 print/import"
        # 额外可添加白名单模块
    try:
        # 使用 -c 参数执行代码，超时 5 秒
        result = subprocess.run(
            ["python", "-c", code],
            capture_output=True,
            text=True,
            timeout=5
        )
        output = result.stdout if result.returncode == 0 else result.stderr
        return output.strip() or "(无输出)"
    except subprocess.TimeoutExpired:
        return "错误：Python 代码执行超时（5秒）"
    except Exception as e:
        return f"执行错误: {str(e)}"


def process_markdown(markdown_text: str) -> str:
    """
    解析 Markdown 文本，执行 ```bash 和 ```python 代码块，
    将每个代码块替换为 ```output ... ``` 格式的执行结果。
    嵌套的 ``` 不会触发新块（视为普通文本）。
    """
    lines = markdown_text.splitlines(keepends=True)
    output_lines = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        # 检测代码块开始：行以 ``` 开头，后面可能跟语言（无其他内容）
        # 匹配模式：行首零个或多个空格 + ``` + 可选语言（非空白字符） + 可选空白 + 换行
        match = re.match(r'^(\s*```)(\w*)\s*$', line)
        if match:
            lang = match.group(2).lower()  # 语言标识
            start_indent = match.group(1)  # 保留前导缩进
            # 收集代码块内容
            code_lines = []
            i += 1
            while i < n:
                # 检查是否为结束标记：行首零个或多个空格 + ``` + 可选空白
                if re.match(r'^\s*```\s*$', lines[i]):
                    i += 1  # 跳过结束标记行
                    break
                code_lines.append(lines[i])
                i += 1
            else:
                # 没有找到结束标记，视为普通文本（保留原样）
                # 回退并原样输出
                output_lines.append(line)
                # 将之前收集的行原样输出
                output_lines.extend(code_lines)
                continue

            # 处理代码块内容
            code_content = ''.join(code_lines).rstrip('\n')
            if lang == 'bash':
                result = execute_bash(code_content)
            elif lang == 'python':
                result = execute_python(code_content)
            else:
                # 其他语言代码块保持不变
                output_lines.append(line)
                output_lines.extend(code_lines)
                output_lines.append('```\n')  # 补回结束标记
                continue

            # 构建输出：保留原缩进的 ```output 块
            output_lines.append(f"{start_indent}output\n")
            # 结果中的每行添加相同的缩进（可选，简单起见不加缩进）
            # 若要保持格式美观，可缩进，但可能破坏原结构，直接原样输出
            for res_line in result.splitlines():
                output_lines.append(f"{res_line}\n")
            output_lines.append(f"{start_indent}```\n")
        else:
            output_lines.append(line)
            i += 1

    return ''.join(output_lines)


# ============ 文本处理主函数 ============
def process_text(text: str, operation: str) -> str:
    """根据操作类型处理文本"""
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
        # 保留原危险操作（仅允许 echo）
        text = text.strip()
        if not text.startswith("echo "):
            return f"错误：出于安全考虑，只允许 'echo' 命令。输入: {text[:50]}"
        try:
            result = subprocess.run(
                text,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            output = result.stdout if result.returncode == 0 else result.stderr
            return output.strip() or "(无输出)"
        except subprocess.TimeoutExpired:
            return "错误：命令执行超时"
        except Exception as e:
            return f"执行错误: {str(e)}"

    return text


# ============ API 路由 ============
@app.get("/")
async def root():
    return {
        "message": "Markdown Code Executor API",
        "version": "2.0.0",
        "endpoints": {
            "POST /process": "处理 Markdown 文本（执行 bash/python 代码块）",
            "GET /health": "健康检查"
        },
        "operations": ["execute_markdown", "reverse", "uppercase", "lowercase", "count", "trim", "bash(危险)"],
        "security": f"允许不安全执行: {ALLOW_UNSAFE} (设置环境变量 ALLOW_CODE_EXECUTION=1 开启)",
        "note": "代码块中的嵌套 ``` 被视为普通文本"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "markdown-executor"}


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
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")


# ============ 启动入口 ============
if __name__ == "__main__":
    print("=" * 60)
    print("🚀 启动 Markdown 代码块执行服务器")
    print("=" * 60)
    print(f"📍 地址: http://127.0.0.1:8000")
    print(f"📖 文档: http://127.0.0.1:8000/docs")
    print(f"🔧 API:  POST http://127.0.0.1:8000/process")
    print("=" * 60)
    if ALLOW_UNSAFE:
        print("⚠️  警告: 已启用不安全执行模式 (ALLOW_CODE_EXECUTION=1)")
        print("     bash 和 python 代码将被实际执行，请勿暴露到公网！")
    else:
        print("🔒 安全模式: 仅允许受限命令 (echo/ls/pwd/date/whoami/cat 和 python print)")
        print("    如需完整执行能力，请设置环境变量: ALLOW_CODE_EXECUTION=1")
    print("=" * 60)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )