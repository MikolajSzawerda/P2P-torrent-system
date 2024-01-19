import asyncio
import logging.config

from .FileManager import FileManager
from .file_client import FileClient

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class DownloadManager:
    def __init__(self, documents_path, file_client: FileClient, file_manager: FileManager):
        self.documents_path = documents_path
        self.file_client = file_client
        self.file_manager = file_manager

    async def download_file(self, file_hash: str, file_name: str, fragments: int):
        self.file_manager.add_document(file_hash, fragments)
        fragments = self.file_manager.get_missing_file_fragments(file_hash)
        # call coordinator
        tasks = [self.file_client.download_fragment(file_hash, frag_id, server_port=12345) for frag_id in fragments]
        await asyncio.gather(*tasks)
        await self.file_manager.merge_fragments(file_hash, file_name)
