import argparse
import asyncio
import logging.config
from concurrent.futures import ThreadPoolExecutor

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from src.DownloadManager import DownloadManager
from src.FileManager import FileManager
from src.coordinator_client import CoordinatorClient
from src.file_client import FileClient
from src.file_server import start_file_sharing

FRAGMENTS_DIR = '../fragments'
DOCUMENTS_DIR = '../documents'
FILE_SERVER_PORT = 6969

logging.config.fileConfig("./client/logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = typer.Typer()
console = Console()


class UI:
    def __init__(self, coordinator_client: CoordinatorClient, file_manager, file_client, download_manager,
                 as_server=True):
        self.coordinator_client = coordinator_client
        self.file_manager = file_manager
        self.file_client = file_client
        self.download_manager = download_manager
        self.as_server = as_server

    @app.command()
    async def list_files(self, file_name: str):
        data = await self.coordinator_client.search_for_file(file_name)
        table = Table("Name", "Hash", "Size")
        for row in data:
            table.add_row(row['id']['name'], row['id']['hash'], str(row['size']))
        console.print(table)
        return {x['id']['hash']: {
            'file_name': x['id']['name'],
            'file_hash': x['id']['hash'],
            'size': x['size'],
        } for x in data}

    @app.command()
    async def download_file(self, file_hash: str, file_name, size: int):
        await self.download_manager.download_file(file_hash, file_name, size)
        await self.coordinator_client.share_new_file(file_name, file_hash, size)

    @app.command()
    async def connect_cmd(self, ):
        files = self.file_manager.get_files_as_dict()
        resp = await self.coordinator_client.connect(files)
        console.print(
            Panel(f"[bold green] Successfully connected to coordinator![/]\n You are sharing: {len(files)} files"))

    @app.command()
    async def statistics(self):
        statistics = await self.coordinator_client.get_statistics()
        return statistics

    async def display_ui(self, loop):
        await self.coordinator_client.start()
        await self.connect_cmd()
        if self.as_server:
            return
        files_cache = {}
        with ThreadPoolExecutor() as pool:
            while True:
                action = await self._input(loop, pool, "[bold red] Action[/]")
                if action == 'list':
                    file_name = await self._input(loop, pool, "File name")
                    files_cache = await self.list_files(file_name)
                elif action == 'download':
                    file_hash = await self._input(loop, pool, "File hash")
                    file_data = files_cache.get(file_hash.strip())
                    if file_data is not None:
                        await self.download_file(**file_data)
                        console.print(Panel(f"[bold green] File downloaded![/]"))

    async def _input(self, loop, pool, prompt):
        return await loop.run_in_executor(pool, lambda: Prompt.ask(prompt))


def arguments():
    parser = argparse.ArgumentParser(description="Torrent client")
    parser.add_argument('--port', type=int, required=True, help='Your file server port')
    parser.add_argument('--chost', type=str, required=True, help='Coordinator host')
    parser.add_argument('--cport', type=int, required=True, help='Coordinator port')
    parser.add_argument('--fragments', type=str, default='fragments', help='Dir of temp')
    parser.add_argument('--documents', type=str, default='documents', help='Dir of docs')
    parser.add_argument('--onlyserver', action='store_true')
    return parser.parse_args()


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_app(loop))


async def run_app(loop):
    args = arguments()
    coordinator_client = CoordinatorClient(args.chost, args.cport, args.port)
    file_manager = FileManager(args.fragments, args.documents)
    file_client = FileClient(file_manager)
    download_manager = DownloadManager(args.documents, file_client, file_manager, coordinator_client)
    ui = UI(coordinator_client, file_manager, file_client, download_manager, args.onlyserver)
    file_registry = await file_manager.get_files_registry()
    await asyncio.gather(
        start_file_sharing(file_registry, args.port),
        ui.display_ui(loop),
    )


if __name__ == "__main__":
    main()
