import socket
import json
from time import sleep


class Client:
    def __init__(self, coordinator_host, coordinator_port):
        self.coordinator_host = coordinator_host
        self.coordinator_port = coordinator_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def format_message(self, action, payload):
        action += " " * (20 - len(action))
        return action + payload

    def connect_and_send_files(self, files_info):
        self.client_socket.connect((self.coordinator_host, self.coordinator_port))
        print(f"Connected to Coordinator at {self.coordinator_host}:{self.coordinator_port}")
        msg = self.format_message("/connect", json.dumps(files_info))
        print(msg)
        self.client_socket.sendall(msg.encode('utf-8'))
        result = self.client_socket.recv(1024).decode("utf-8")
        print(result)

    def close_connection(self):
        self.client_socket.sendall('/close'.encode('utf-8'))
        self.client_socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    client = Client('127.0.0.1', 65432)
    client.connect_and_send_files({
        'files': [
            # {"name": "file.txt", "md5": "hdyz", "num_segments": 5},
            {"name": "file.txt", "md5": "hdyz", "num_segments": 5}
            # {"name": "file2.txt", "md5": "hdyz2", "num_segments": 5, "owned_segments": [0, 1, 2]},
        ]
    })
    sleep(2)
    client.close_connection()
