import asyncio
import websockets
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

# 存储所有活跃的WebSocket客户端连接
clients = set()

async def websocket_handler(websocket, path):
    """处理WebSocket连接：接收消息并广播"""
    clients.add(websocket)
    try:
        async for message in websocket:
            print(f"收到消息: {message}")
            # 广播消息给所有客户端（可选）
            await broadcast(f"转发: {message}")
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        clients.remove(websocket)

async def broadcast(message):
    """向所有客户端广播消息"""
    if clients:
        await asyncio.gather(*[client.send(message) for client in clients])

async def hourly_task():
    """每小时整点执行的任务"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 开始执行定时任务")
    # 示例：向所有客户端发送系统通知
    await broadcast("系统通知：整点数据已更新！")

async def main():
    """主函数：启动WebSocket服务与定时任务"""
    # 启动WebSocket服务器（端口8765）
    server = await websockets.serve(websocket_handler, "localhost", 8765)
    print("WebSocket服务器已启动，监听端口 8765")

    # 配置APScheduler定时任务（每小时0分触发）
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        hourly_task,
        trigger=IntervalTrigger(seconds=1),  # 每小时第0秒触发
        timezone="Asia/Shanghai"         # 根据需求设置时区
    )
    scheduler.start()
    print("定时任务已启动，将在每小时整点执行")

    # 保持程序持续运行
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())