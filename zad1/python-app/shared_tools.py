import io


def prepare_message(message: str) -> bytes:
    binary_stream = io.BytesIO()
    binary_stream.write(message.encode('ascii'))
    binary_stream.seek(0)
    stream_data = binary_stream.read()
    return stream_data

def get_n_of_alphabet(length: int) -> str:
    if length > 26:
        raise ValueError('length must be less than 26')
    return ''.join([chr(i) for i in range(ord('A'), ord('A') + length)])
def get_alphanet_message(length: int) -> str:
    full_alphabets = length // 26
    remainder = length % 26
    return get_n_of_alphabet(26) * full_alphabets + get_n_of_alphabet(remainder)
