import logging
import json
from asyncio import StreamReader, StreamWriter

from typing import Any, TypeAlias

from coordinator.src.schema import Command

logger = logging.getLogger(__name__)

ClientId: TypeAlias = str


class ClientIsNotConnectedError(Exception):
    pass


class ConnectedClient:
    CHUNK_SIZE = 4096

    def __init__(
        self, reader: StreamReader, writer: StreamWriter, address: ClientId
    ) -> None:
        self._reader = reader
        self._writer = writer
        self._address = address

    @property
    def id(self) -> ClientId:
        return self._address

    async def send(self, data: Any) -> None:
        serialized_data = json.dumps(data).encode()

        self._writer.write(serialized_data)
        await self._writer.drain()

    async def send_success_response(self) -> None:
        await self.send({"status": "success"})

    async def send_error_response(self) -> None:
        await self.send({"status": "error"})

    async def read_command(self) -> Command | None:
        data = await self._reader.read(ConnectedClient.CHUNK_SIZE)
        if not data:
            raise ClientIsNotConnectedError(f"Client {self.id} is not connected anymore")

        try:
            data_json = json.loads(data)
        except json.decoder.JSONDecodeError:
            logger.error("%s is not a valid command", data.decode())
            return None

        return Command.from_dict(data_json)

    async def disconnect(self) -> None:
        self._writer.close()
        await self._writer.wait_closed()

    def __eq__(self, other: Any):
        return isinstance(other, ConnectedClient) and self.id == other.id
