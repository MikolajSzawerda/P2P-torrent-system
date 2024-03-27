import logging
import asyncio
import struct

from .constants import *

logger = logging.getLogger(__name__)


async def read_header(reader: asyncio.StreamReader) -> MsgHeader | None:
    common_header = await reader.readexactly(COMMON_HEADER_LEN)
    if not common_header:
        return None
    m_type, m_len, m_frag, m_hash = struct.unpack(COMMON_HEADER_SCHEME, common_header)
    return MsgHeader(m_type, m_len, m_frag, m_hash.decode())


def serialize_header(header: MsgHeader) -> bytes:
    return struct.pack(COMMON_HEADER_SCHEME, header.type, header.length, header.fragment_id, header.hash.encode())
