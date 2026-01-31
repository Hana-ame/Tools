import socket
import threading
import argparse


def print(str):
    return


def forward_data(local_conn, remote_conn):
    try:
        while True:
            data = local_conn.recv(4096)
            if not data:
                break
            remote_conn.sendall(data)
    except Exception as e:
        print(f"Error forwarding data: {e}")
    finally:
        local_conn.close()
        remote_conn.close()


def handle_client(client_conn, remote_host, remote_port):
    try:
        # Determine the address family for the remote host
        remote_addr_info = socket.getaddrinfo(
            remote_host, remote_port, socket.AF_UNSPEC, socket.SOCK_STREAM
        )
        if not remote_addr_info:
            raise socket.gaierror("No address information for remote host")

        # Use the first available address information
        remote_family, remote_type, _, _, remote_addr = remote_addr_info[0]

        # Create a connection to the remote host
        remote_conn = socket.socket(remote_family, remote_type)
        remote_conn.connect(remote_addr)

        # Start forwarding data from client to remote and vice versa
        client_to_remote_thread = threading.Thread(
            target=forward_data, args=(client_conn, remote_conn)
        )
        remote_to_client_thread = threading.Thread(
            target=forward_data, args=(remote_conn, client_conn)
        )

        client_to_remote_thread.start()
        remote_to_client_thread.start()

        # Wait for both threads to finish
        client_to_remote_thread.join()
        remote_to_client_thread.join()
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_conn.close()


def start_server(local_host, local_port, remote_host, remote_port):
    server = None  # Initialize first

    try:
        # Determine the address family for the local host
        local_addr_info = socket.getaddrinfo(
            local_host, local_port, socket.AF_UNSPEC, socket.SOCK_STREAM
        )
        if not local_addr_info:
            raise socket.gaierror("No address information for local host")

        # Use the first available address information
        local_family, local_type, _, _, local_addr = local_addr_info[0]

        # Create and bind the server socket
        server = socket.socket(local_family, local_type)
        server.bind(local_addr)
        server.listen(5)
        print(
            f"Listening on {local_host}:{local_port} and forwarding to {remote_host}:{remote_port}"
        )

        while True:
            client_conn, addr = server.accept()
            print(f"Accepted connection from {addr}")
            client_handler_thread = threading.Thread(
                target=handle_client, args=(client_conn, remote_host, remote_port)
            )
            client_handler_thread.start()
    except KeyboardInterrupt:
        print("Server shutting down.")
    except Exception as e:
        print(f"Error starting server: {e}")
    finally:
        if server:
            server.close()


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Port Forwarding Script")
    parser.add_argument(
        "--local-host",
        type=str,
        default="2001:470:c:6c::2",
        help="Local host address (IPv6)",
    )
    parser.add_argument(
        "--local-port", type=int, default=443, help="Local port to listen on"
    )
    parser.add_argument(
        "--remote-host", type=str, default="127.0.0.1", help="Remote host address"
    )
    parser.add_argument(
        "--remote-port", type=int, default=443, help="Remote port to forward to"
    )

    # Parse arguments
    args = parser.parse_args()

    print(args)

    # Start the server with the provided arguments
    start_server(args.local_host, args.local_port, args.remote_host, args.remote_port)
