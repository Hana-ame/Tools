#!/bin/bash

# 使用说明函数
usage() {
    echo "用法: $0 -t <任务名> -s <启动脚本路径>"
    echo "示例: $0 -t my_app -s /home/user/start_my_app.sh"
    exit 1
}

# 参数检查：如果参数个数不为4，显示用法说明
if [ $# -ne 4 ]; then
    usage
fi

# 使用 getopts 处理命令行选项
while getopts "t:s:" opt; do
    case $opt in
        t)
            TASK_NAME="$OPTARG"  # 要监控的进程名
            ;;
        s)
            START_SCRIPT="$OPTARG"  # 启动脚本的路径
            ;;
        \?)
            echo "无效的选项: -$OPTARG" >&2
            usage
            ;;
        :)
            echo "选项 -$OPTARG 需要一个参数." >&2
            usage
            ;;
    esac
done

# 检查必要的参数是否提供
if [ -z "$TASK_NAME" ] || [ -z "$START_SCRIPT" ]; then
    echo "错误：任务名和启动脚本路径为必填项。"
    usage
fi

# 日志文件路径（可以自定义，这里固定为与脚本同目录的 monitor.log）
LOG_FILE="$(dirname "$0")/monitor_${TASK_NAME}.log"

# 获取当前时间并格式化
current_time=$(date "+%Y-%m-%d %H:%M:%S")

# 使用 pgrep 检查进程是否存在
if pgrep -x "$TASK_NAME" > /dev/null; then
    # 进程存在
    echo "$current_time Task '$TASK_NAME' is RUNNING." >> "$LOG_FILE"
else
    # 进程不存在，尝试启动
    echo "$current_time Task '$TASK_NAME' is NOT running. Attempting to restart..." >> "$LOG_FILE"
    
    # 检查启动脚本是否存在且可执行
    if [ ! -f "$START_SCRIPT" ]; then
        echo "$current_time ERROR: Startup script '$START_SCRIPT' not found!" >> "$LOG_FILE"
        exit 1
    fi
    if [ ! -x "$START_SCRIPT" ]; then
        echo "$current_time WARNING: Startup script '$START_SCRIPT' is not executable. Trying to run with bash..." 
        # 如果启动脚本本身没有可执行权限，尝试用 bash 执行
        bash "$START_SCRIPT" >> "$LOG_FILE" 2>&1
    else
        # 如果脚本有可执行权限，直接执行
        "$START_SCRIPT" >> "$LOG_FILE" 2>&1
    fi

    # 稍作等待，然后检查进程是否启动成功
    sleep 3
    new_pid=$(pgrep -x "$TASK_NAME" 2>/dev/null)
    
    if [ -n "$new_pid" ]; then
        echo "$current_time Task '$TASK_NAME' restarted SUCCESSFULLY. New PID: $new_pid" >> "$LOG_FILE"
    else
        echo "$current_time ERROR: Failed to restart '$TASK_NAME'." >> "$LOG_FILE"
    fi
fi


