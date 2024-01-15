import socket
import json
from time import sleep


class Client:
    def __init__(self, coordinator_host, coordinator_port):
        self.coordinator_host = coordinator_host
        self.coordinator_port = coordinator_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_and_send_files(self, files_info):
        self.client_socket.connect((self.coordinator_host, self.coordinator_port))
        print(f"Connected to Coordinator at {self.coordinator_host}:{self.coordinator_port}")

        self.client_socket.sendall('/connect'.encode('utf-8'))
        ack = self.client_socket.recv(1024).decode('utf-8')
        print(ack)
        message = json.dumps(files_info)
        self.client_socket.sendall(message.encode('utf-8'))

    def close_connection(self):
        self.client_socket.sendall('/close'.encode('utf-8'))
        self.client_socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    client = Client('127.0.0.1', 65432)
    client.connect_and_send_files({
        'files': [
            {'name': 'file.txt', 'md5': '9e107d9d372bb6826bd81d3542a419d6'},
            {'name': 'video.mp4', 'md5': 'a54d88e06612d820bc3be72877c74f257'}
        ]
    })
    sleep(2)
    client.close_connection()
