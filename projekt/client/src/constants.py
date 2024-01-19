from dataclasses import dataclass

FRAGMENT_SIZE = 80
MSG_DATA_REQUEST = 0
MSG_DATA_TRANSFER = 1
COMMON_HEADER_SCHEME = '>B I I'  # msg_type, length, fragment_id
COMMON_HEADER_LEN = 1 + 4 + 4
TRANSFER_HEADER = '> 32s'  # data hash
TRANSFER_HEADER_FULL = '> B I I 32s'  # data hash
TRANSFER_HEADER_LEN = 32


@dataclass(eq=True, frozen=True)
class MsgHeader:
    type: int
    length: int
    fragment_id: int
    hash: bytes  # optional

    def has_data(self) -> bool:
        return self.length > 0

    def is_request(self) -> bool:
        return self.type == MSG_DATA_REQUEST


@dataclass(eq=True, frozen=True)
class Document:
    name: str
    path: str
    hash: str
    fragments: int
