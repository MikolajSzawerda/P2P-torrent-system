import asyncio
import json


class CoordinatorClient:
    def __init__(self, host, port, server_port):
        self.host = host
        self.port = port
        self.server_port = server_port
        self.reader = None
        self.writer = None

    async def start(self):
        reader, writer = await asyncio.open_connection('localhost', 65432)
        self.reader = reader
        self.writer = writer

    async def connect(self, files_list):
        self.writer.write(json.dumps({
            'route': 'connect',
            'payload': {
                'server_port': self.server_port,
                'files': files_list
            }
        }).encode())
        await self.writer.drain()
        return await self.reader.read(1024)

    async def search_for_file(self, name: str):
        self.writer.write(json.dumps({
            'route': 'search_by_name',
            'payload': {
                'name': name
            }
        }).encode())
        await self.writer.drain()
        resp = await self.reader.read(4096)
        return json.loads(resp.decode())

    async def get_file_fragments(self, file_name, file_hash, fragments) -> dict[int, tuple[str, int]]:
        self.writer.write(json.dumps({
            "route": "assign_segments",
            "payload": {"name": file_name, "hash": file_hash, "segment_ids": [x - 1 for x in fragments]}
        }).encode())
        await self.writer.drain()
        resp = await self.reader.read(4096)
        return json.loads(resp.decode())
