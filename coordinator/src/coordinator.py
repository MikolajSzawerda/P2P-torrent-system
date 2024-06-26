import datetime
import logging
from collections import defaultdict

from .connected_client import ClientId
from .schema import File, FileId
from .statistics import Statistics

logger = logging.getLogger(__name__)


class Coordinator:
    def __init__(self, statistics: Statistics = Statistics()) -> None:
        self._clients: dict[ClientId, set[FileId]] = defaultdict(set)
        self._client_last_assignment: dict[ClientId, float] = {}

        self._files: dict[FileId, File] = {}
        self._file_owners: dict[FileId, set[ClientId]] = defaultdict(set)
        self._client_server_ports: dict[ClientId, int] = {}

    
        self._statistics = statistics

    def connect_client(self, client_id: ClientId, files: list[File], server_port=0) -> None:
        if client_id in self._clients:
            raise ValueError(f"Client {client_id} is already connected.")

        valid_files = [file for file in files if self._is_valid_file(file)]

        if len(files) != len(valid_files):
            logger.warning(
                "%s out of %s shared files by %s are invalid",
                client_id,
                len(files) - len(valid_files),
                len(files)
            )

        self._clients[client_id] = {file.id for file in valid_files}
        self._client_last_assignment[client_id] = self._get_current_timestamp()
        self._client_server_ports[client_id] = server_port
        self._statistics.update_on_connect(len(self._clients))

        for file in valid_files:
            self._files[file.id] = file
            self._file_owners[file.id].add(client_id)

    def share_file(self, client_id: ClientId, file: File) -> None:
        self._assert_client_is_connected(client_id)

        if not self._is_valid_file(file):
            logger.warning("Client %s shared an invalid file", client_id)
            return

        self._clients[client_id].add(file.id)
        self._files[file.id] = file
        self._file_owners[file.id].add(client_id)
        self._statistics.update_shared_files(1)

    def disconnect_client(self, client_id: ClientId) -> None:
        self._assert_client_is_connected(client_id)

        client_files = self._clients.pop(client_id)
        self._client_server_ports.pop(client_id)
        for file_id in client_files:
            if len(self._file_owners[file_id]) == 1:
                self._files.pop(file_id)
                self._file_owners.pop(file_id)
            else:
                self._file_owners[file_id].remove(client_id)

        self._statistics.update_on_disconnect()

    def search_by_name(self, name: str) -> list[File]:
        return list(filter(lambda file: file.id.name == name, self._files.values()))

    def assign_segments(
            self, file_id: FileId, requested_segments: list[int]
    ) -> dict[int, tuple[str, int]]:
        file = self._files.get(file_id)

        if file is None:
            logger.warning("Requested file %s doesn't exist", file_id)
            return {}

        if min(requested_segments) < 0 or max(requested_segments) >= file.segments:
            logger.warning(
                "Requested invalid segments. File %s has %s segments",
                file_id,
                file.segments
            )
            return {}

        assignment = {}
        file_owners = self._file_owners[file_id]
        self._statistics.update_on_file_request(len(file_owners))

        for seg in requested_segments:
            assigned_owner_id = min(file_owners, key=self._client_last_assignment.get)

            assignment[seg] = (assigned_owner_id[0], self._client_server_ports[assigned_owner_id])
            self._client_last_assignment[assigned_owner_id] = self._get_current_timestamp()

        return assignment

    def generate_stats(self) -> str:
        return self._statistics.generate_report()

    def _is_valid_file(self, file: File) -> bool:
        if file.id in self._files and self._files[file.id] != file:
            self._statistics.update_invalid_files(1)
            return False

        return True

    def _assert_client_is_connected(self, client_id: ClientId) -> None:
        if client_id not in self._clients:
            raise ValueError(f"Client {client_id} is not connected.")

    @staticmethod
    def _get_current_timestamp() -> float:
        return datetime.datetime.now().timestamp()
