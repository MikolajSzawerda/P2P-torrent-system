import hashlib
import logging
from typing import Dict

from .file_store import get_file_fragment
from .serde import *

logger = logging.getLogger(__name__)
example_data = "data_test"


async def _send_file_stream(file_path, fragment_id: int, writer: asyncio.StreamWriter):
    data = await get_file_fragment(file_path, fragment_id)
    receiver_header = MsgHeader(MSG_DATA_TRANSFER, FRAGMENT_SIZE, fragment_id, hashlib.md5(data).hexdigest())
    writer.write(serialize_header(receiver_header))
    writer.write(data)
    logger.info("Sent data transfer %s", receiver_header)
    await writer.drain()


async def _handle_file_share(reader: asyncio.StreamReader, writer: asyncio.StreamWriter, registry: Dict[str, Document]):
    address = writer.get_extra_info('peername')
    while True:
        header = await read_header(reader)
        logger.info("Received request %s from %s", header, address)
        if not header:
            logger.info("End of data stream")
            break
        if not header.is_request():
            logger.warning("Not supported message type %d", header.type)
            break
        file_path = registry.get(header.hash).path
        await _send_file_stream(file_path, header.fragment_id, writer)
    logger.info("Transfer to %s ended", address)
    writer.close()
    await writer.wait_closed()


async def start_file_sharing(registry: Dict[str, Document], port: int):
    async def file_share_func(reader, writer):
        return await _handle_file_share(reader, writer, registry)

    server = await asyncio.start_server(file_share_func, host='localhost', port=port)
    addr = server.sockets[0].getsockname()
    logger.info("Started client file server on %s", addr)
    async with server:
        await server.serve_forever()
