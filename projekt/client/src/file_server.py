import hashlib
import logging
import os

import aiofiles

from .serde import *

logger = logging.getLogger(__name__)
example_data = "data_test"
file_path = "/documents/example_file.txt"


async def _send_file_stream(header: MsgHeader, writer: asyncio.StreamWriter):
    file_size = os.path.getsize(file_path)
    receiver_header = MsgHeader(MSG_DATA_TRANSFER, file_size, header.fragment_id,
                                hashlib.sha256(example_data.encode()).digest())
    writer.write(serialize_transfer_header(receiver_header))
    async with aiofiles.open(file_path, 'rb') as file:
        data = await file.read(file_size)
        writer.write(data)
        await writer.drain()
    await writer.drain()


async def _handle_file_share(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    address = writer.get_extra_info('peername')
    logger.info("New connection from %s", address)
    while True:
        header = await read_header(reader)
        if not header:
            logger.info("End of data stream")
            break
        if not header.is_request():
            logger.warning("Not supported message type %d", header.type)
            break
        await _send_file_stream(header, writer)
    logger.info("Transfer to %s ended", address)
    writer.close()
    await writer.wait_closed()


async def start_file_sharing(port: int):
    server = await asyncio.start_server(_handle_file_share, host='localhost', port=port)
    addr = server.sockets[0].getsockname()
    logger.info("Started client file server on %s", addr)
    async with server:
        await server.serve_forever()
