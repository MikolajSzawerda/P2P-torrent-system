import asyncio
import logging.config
from math import ceil

from .FileManager import FileManager
from .constants import FRAGMENT_SIZE
from .coordinator_client import CoordinatorClient
from .file_client import FileClient

logger = logging.getLogger(__name__)


class DownloadManager:
    def __init__(self, documents_path, file_client: FileClient, file_manager: FileManager,
                 coordinator_client: CoordinatorClient):
        self.documents_path = documents_path
        self.file_client = file_client
        self.file_manager = file_manager
        self.coordinator_client = coordinator_client

    async def download_file(self, file_hash: str, file_name: str, size: int):
        fragments = ceil(size / FRAGMENT_SIZE)
        self.file_manager.add_document(file_hash, fragments)
        fragments = self.file_manager.get_missing_file_fragments(file_hash)
        data = await self.coordinator_client.get_file_fragments(file_name, file_hash, fragments)
        tasks = [self.file_client.download_fragment(file_hash, int(frag_id) + 1, server_port=port, server_ip=host) for
                 (frag_id, (host, port)) in data.items()]

        await asyncio.gather(*tasks)
        await self.file_manager.merge_fragments(file_hash, file_name)
