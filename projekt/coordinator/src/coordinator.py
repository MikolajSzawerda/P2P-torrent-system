import datetime

from coordinator.src.connected_client import ConnectedClient, ClientId
from coordinator.src.repository import Repository, FileFormatException
from coordinator.src.schema import File, FileId


class Coordinator:
    def __init__(self, repository: Repository):
        self._repo = repository

        self._files: dict[FileId, File] = {}
        self._file_segments: dict[FileId, dict[int, list[ClientId]]] = {}

        self._clients: dict[ClientId, ConnectedClient] = {}
        self._client_last_assignment: dict[ClientId, int] = {}

    def connect_client(self, client: ConnectedClient) -> None:
        self._clients[client.id] = client

    def disconnect_client(self, client: ConnectedClient) -> None:
        self._clients.pop(client.id)

    def search_by_name(self, name: str) -> list[File]:
        return list(filter(lambda file: file.id.name == name, self._files.values()))

    def assign_segments(self, file_id: FileId, segment_ids) -> dict[int, ClientId]:
        assignment = {}

        for seg in segment_ids:
            owner_ids = self._file_segments[file_id][seg]
            if not owner_ids:
                continue

            assigned_owner_id = sorted(owner_ids, key=lambda id_: self._file_segments.get(id_, 0))[0]

            assignment[seg] = assigned_owner_id
            self._client_last_assignment[assigned_owner_id] = int(datetime.datetime.now().timestamp())

        return assignment

    # def handle_message(self, message, client_socket, client_address):
    #     action = message[:30]
    #
    #     if action.startswith("/connect"):
    #         try:
    #             payload = json.loads(message[30:])
    #             self._repo.add_client(client_address, payload["files"])
    #             print(f"Client added to db {client_address}")
    #             client_socket.sendall("success".encode("utf-8"))
    #         except FileFormatException as e:
    #             client_socket.sendall(str(e).encode("utf-8"))
    #             print(f"Failed connect attempt of {client_address}")
    #             raise ExitClient()
    #         # print(self.db.get_all_data())
    #     elif action.startswith("/search_by_name"):
    #         payload = json.loads(message[30:])
    #         files = self._repo.get_files_by_name(payload["name"])
    #         client_socket.sendall(json.dumps(files).encode("utf-8"))
    #     elif action.startswith("/search_by_md5"):
    #         payload = json.loads(message[30:])
    #         files = self._repo.get_files_by_md5(payload["md5"])
    #         client_socket.sendall(json.dumps(files).encode("utf-8"))
    #     elif action.startswith("/search_by_name_md5"):
    #         payload = json.loads(message[30:])
    #         files = self._repo.get_files_by_name_and_md5(
    #             payload["name"], payload["md5"]
    #         )
    #         client_socket.sendall(json.dumps(files).encode("utf-8"))
    #     elif action.startswith("/get_owner_of_segment"):
    #         payload = json.loads(message[30:])
    #         client = self._repo.get_client_with_file(
    #             payload["name"], payload["md5"], payload["segment_number"]
    #         )
    #         client_socket.sendall(json.dumps(client).encode("utf-8"))
    #     elif action.startswith("/update_client"):
    #         payload = json.loads(message[30:])
    #         self._repo.add_client(client_address, payload["files"])
    #         client_socket.sendall("success".encode("utf-8"))
    #     elif action.startswith("/close"):
    #         print(f"Closing connection with {client_address}")
    #         raise ExitClient()
    #     else:
    #         print("cannot handle")
