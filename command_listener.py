
import socket
import threading

class CommandListener(threading.Thread):
    def __init__(self, host='localhost', port=12345):
        super().__init__()
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Listening on {self.host}:{self.port}...")

        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Connection from {addr} established.")
            self.handle_client(client_socket)

    def handle_client(self, client_socket):
        with client_socket:
            while True:
                command = client_socket.recv(1024).decode('utf-8')
                if not command:
                    break
                print(f"Received command: {command}")
                try:
                    # 使用 eval 执行接收到的命令
                    result = eval(command,globals())
                    client_socket.sendall(str(result).encode('utf-8'))
                except Exception as e:
                    client_socket.sendall(f"Error: {str(e)}".encode('utf-8'))
                client_socket.sendall(b"\n")

# 要在main module里面，不然没用
if __name__ == "__main__":
    
    # 创建并启动 CommandListener 线程
    command_listener = CommandListener(port=12345)
    command_listener.daemon = True  # 设置为守护线程
    command_listener.start()
