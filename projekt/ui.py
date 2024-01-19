import typer
import asyncio
import logging.config

from client.src.DownloadManager import DownloadManager
from client.src.FileManager import FileManager
from client.src.file_client import FileClient
from client.src.file_server import start_file_sharing

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = typer.Typer()


async def show_available_files(file_manager: FileManager):
    file_registry = await file_manager.get_files_registry()
    logger.info("Available files: %s", [x.name for x in file_registry.values()])


async def connect(port: int):
    file_manager = FileManager("fragments", "../documents")

    async def main():
        file_registry = await file_manager.get_files_registry()
        await show_available_files(file_manager)
        if port == 6969:
            await asyncio.run(start_file_sharing(file_registry, port))
        else:
            await start_file_sharing(file_registry, port)

    await main()


async def download(file_hash: str, file_name: str, fragment_id: int, download_manager: DownloadManager):
    await download_manager.download_file(file_hash, file_name, fragment_id)


@app.command()
def connect_cmd(port: int = 6969):
    asyncio.run(connect(port))


@app.command()
def list_files():
    file_manager = FileManager("fragments", "../documents")
    asyncio.run(show_available_files(file_manager))


@app.command()
def download_cmd(file_hash: str = "b157e8529683a2da7e5e675340a48f6b", file_name: str = "test2.txt", fragment_id: int = 2):
    file_manager = FileManager("fragments", "../documents")
    file_client = FileClient(file_manager)
    download_manager = DownloadManager("../documents", file_client, file_manager)
    asyncio.run(download(file_hash, file_name, fragment_id, download_manager))


if __name__ == '__main__':
    app()
