import asyncio
import logging
from asyncio import StreamWriter, StreamReader

from coordinator.src.connected_client import ConnectedClient, ClientIsNotConnectedError
from coordinator.src.routes_registry import RoutesRegistry

logger = logging.getLogger(__name__)


class ServerRunner:
    def __init__(self, router: RoutesRegistry, host: str, port: int) -> None:
        self._router = router
        self._host = host
        self._port = port

    def start(self):
        asyncio.run(self._start())

    async def _start(self):
        server = await asyncio.start_server(
            self._accept_new_client, self._host, self._port
        )
        logger.info("Server started listening on %s:%s", self._host, self._port)

        async with server:
            await server.serve_forever()

    async def _accept_new_client(
        self, reader: StreamReader, writer: StreamWriter
    ) -> None:
        address = writer.get_extra_info("peername")
        logger.info("Accepted a new connection from %s", address)

        client = ConnectedClient(reader, writer, address)

        try:
            await self._handle_client(client)
        finally:
            await self._router.run_handler("disconnect", client=client)

    async def _handle_client(self, client: ConnectedClient) -> None:
        while True:
            try:
                command = await client.read_command()
            except ClientIsNotConnectedError:
                break

            if not command:
                await asyncio.sleep(0.2)
                continue

            try:
                await self._router.run_handler(
                    command.route, client=client, **command.payload
                )
            except Exception as e:
                logger.error("Error while handling command %s. Error: %s", command, e)
