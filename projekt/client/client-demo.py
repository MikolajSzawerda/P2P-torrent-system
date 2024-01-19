import asyncio
import logging.config
import sys

from src.DownloadManager import DownloadManager
from src.FileManager import FileManager
from src.file_client import FileClient
from src.file_server import start_file_sharing

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


async def example_client_flow(download_manager: DownloadManager):
    await asyncio.sleep(1)
    await download_manager.download_file("b157e8529683a2da7e5e675340a48f6b", "test.txt", 2)


async def main():
    port = int(sys.argv[1])
    other_port = int(sys.argv[2])
    file_manager = FileManager("fragments",
                               "../documents")
    file_client = FileClient(file_manager)
    download_manager = DownloadManager("../documents", file_client,
                                       file_manager)
    file_registry = await file_manager.get_files_registry()
    logger.info("Available files: %s", [x.name for x in file_registry.values()])
    if port == 6969:
        await asyncio.gather(
            start_file_sharing(file_registry, port),
            example_client_flow(download_manager)
        )
    else:
        await start_file_sharing(file_registry, port)


if __name__ == '__main__':
    asyncio.run(main())
