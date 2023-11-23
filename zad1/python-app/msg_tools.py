import io
from config import LENGTH_SPACE

def get_n_of_alphabet(length: int) -> str:
    if length > 26:
        raise ValueError('length must be less than 26')
    return ''.join([chr(i) for i in range(ord('A'), ord('A') + length)])


def get_alphabet_payload(length: int) -> str:
    full_alphabets = length // 26
    remainder = length % 26
    return get_n_of_alphabet(26) * full_alphabets + get_n_of_alphabet(remainder)


def verify_message(message: bytes) -> bool:
    binary_stream = io.BytesIO(message)
    length = int.from_bytes(binary_stream.read(LENGTH_SPACE), byteorder='little')
    return message[LENGTH_SPACE:].decode('ascii') == get_alphabet_payload(length - LENGTH_SPACE)


def prepare_proper_message(length: int) -> bytes:
    return length.to_bytes(LENGTH_SPACE, byteorder='little') + get_alphabet_payload(length - LENGTH_SPACE).encode('ascii')

def prepare_other_content_message(length: int) -> bytes:
    reversed_alphabet = get_alphabet_payload(length - LENGTH_SPACE)[::-1]
    return length.to_bytes(LENGTH_SPACE, byteorder='little') + reversed_alphabet.encode(
        'ascii')
def prepare_other_length_message(length: int) -> bytes:
    return length.to_bytes(LENGTH_SPACE, byteorder='little') + get_alphabet_payload(length + 3 - LENGTH_SPACE).encode('ascii')
