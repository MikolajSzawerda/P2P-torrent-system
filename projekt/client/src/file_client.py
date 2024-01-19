import logging

from .FileManager import FileManager
from .serde import *

logger = logging.getLogger(__name__)


async def _send_file_request(file_hash: str, fragment_id: int, writer: asyncio.StreamWriter):
    request_header = MsgHeader(MSG_DATA_REQUEST, 0, fragment_id, file_hash)
    logger.info("Sending request for file %s and fragment %s", request_header.hash, request_header.fragment_id)
    writer.write(serialize_header(request_header))
    await writer.drain()


class FileClient:
    def __init__(self, file_manager: FileManager):
        self._file_manager = file_manager

    async def _read_transfer_message(self, file_hash, reader: asyncio.StreamReader):
        header = await read_header(reader)
        if not header or not header.has_data():
            logger.info("End of data stream")
            return
        if header.is_request():
            logger.warning("Not supported message type %d", header.type)
            return
        data = await reader.readexactly(header.length)
        await self._file_manager.add_fragment(file_hash, header.fragment_id, data)
        logger.info("Fragment transfer end")

    async def download_fragment(self, file_hash, fragment_id, server_ip='127.0.0.1', server_port=8888):
        reader, writer = await asyncio.open_connection(server_ip, server_port)
        await _send_file_request(file_hash, fragment_id, writer)
        await self._read_transfer_message(file_hash, reader)
        writer.close()
        await writer.wait_closed()
