import logging

from .file_store import save_fragment
from .serde import *

logger = logging.getLogger(__name__)


async def _send_file_request(writer: asyncio.StreamWriter):
    request_header = MsgHeader(MSG_DATA_REQUEST, 0, 1, bytes("", 'utf-8'))
    writer.write(serialize_request_header(request_header))
    await writer.drain()


async def _read_transfer_message(reader: asyncio.StreamReader):
    header = await read_header(reader)
    if not header or not header.has_data():
        logger.info("End of data stream")
        return
    if header.is_request():
        logger.warning("Not supported message type %d", header.type)
        return
    data = await reader.readexactly(header.length)
    await save_fragment("test", header.fragment_id, data)
    logger.info("Fragment transfer end")


async def download_fragment(server_ip='127.0.0.1', server_port=8888):
    await asyncio.sleep(1)  # Hack when running multiple clients at once
    reader, writer = await asyncio.open_connection(server_ip, server_port)
    await _send_file_request(writer)
    await _read_transfer_message(reader)
    writer.close()
    await writer.wait_closed()
