import asyncio
import struct

from .constants import *


async def read_header(reader: asyncio.StreamReader) -> MsgHeader | None:
    common_header = await reader.readexactly(COMMON_HEADER_LEN)
    if not common_header:
        return None
    m_type, m_len, m_frag = struct.unpack(COMMON_HEADER_SCHEME, common_header)
    if m_type == MSG_DATA_REQUEST:
        return MsgHeader(m_type, m_len, m_frag, 0)
    transfer_header = await reader.readexactly(TRANSFER_HEADER_LEN)
    if not transfer_header:
        return None
    m_hash = struct.unpack(TRANSFER_HEADER, transfer_header)
    return MsgHeader(m_type, m_len, m_frag, m_hash[0])


def serialize_transfer_header(header: MsgHeader) -> bytes:
    return struct.pack(TRANSFER_HEADER_FULL, header.type, header.length, header.fragment_id, header.hash)


def serialize_request_header(header: MsgHeader) -> bytes:
    return struct.pack(COMMON_HEADER_SCHEME, header.type, header.length, header.fragment_id)
