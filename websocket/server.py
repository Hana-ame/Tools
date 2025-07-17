import asyncio
import websockets

async def handler(websocket, path):
    async for message in websocket:
        print(f"收到消息: {message}")
        await websocket.send(f"已回复: {message}")  # 回显消息

# 启动服务器
async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # 永久运行

asyncio.run(main())