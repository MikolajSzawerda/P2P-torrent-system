import argparse
import asyncio
import logging.config

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from client.src.DownloadManager import DownloadManager
from client.src.FileManager import FileManager
from client.src.coordinator_client import CoordinatorClient
from client.src.file_client import FileClient
from client.src.file_server import start_file_sharing

FRAGMENTS_DIR = 'fragments'
DOCUMENTS_DIR = 'documents'
FILE_SERVER_PORT = 6969

logging.config.fileConfig("client/logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = typer.Typer()
console = Console()


class UI:
    def __init__(self, coordinator_client, file_manager, file_client, download_manager, as_server=True):
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

    async def display_ui(self):
        await self.coordinator_client.start()
        await self.connect_cmd()
        if self.as_server:
            return
        files_cache = {}
        while True:
            action = Prompt.ask("[bold red] Action[/]")
            if action == 'list':
                file_name = Prompt.ask("File name")
                files_cache = await self.list_files(file_name)
            elif action == 'download':
                file_hash = Prompt.ask("File hash")
                file_data = files_cache.get(file_hash.strip())
                if file_data is not None:
                    await self.download_file(**file_data)
                    console.print(Panel(f"[bold green] File downloaded![/]"))
            elif action == 'statistics':
                statistics = await self.statistics()
                console.print(statistics)


def arguments():
    parser = argparse.ArgumentParser(description="Example script with named arguments.")
    parser.add_argument('--port', type=int, required=True, help='Your name')
    parser.add_argument('--fragments', type=str, default='fragments', help='Your name')
    parser.add_argument('--documents', type=str, default='documents', help='Your age (default: 30)')
    parser.add_argument('--onlyserver', action='store_true', help='Your age (default: 30)')
    return parser.parse_args()


async def main():
    args = arguments()
    coordinator_client = CoordinatorClient('', '', args.port)
    file_manager = FileManager(args.fragments, args.documents)
    file_client = FileClient(file_manager)
    download_manager = DownloadManager(args.documents, file_client, file_manager, coordinator_client)
    ui = UI(coordinator_client, file_manager, file_client, download_manager, args.onlyserver)
    file_registry = await file_manager.get_files_registry()
    await asyncio.gather(
        ui.display_ui(),
        start_file_sharing(file_registry, args.port)
    )


if __name__ == "__main__":
    asyncio.run(main())
