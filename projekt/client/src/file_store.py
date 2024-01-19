import asyncio
import hashlib
import os
from typing import Dict

import aiofiles

from .constants import FRAGMENT_SIZE, Document


async def save_fragment(file_id, fragment_id, data):
    directory = f"fragments/{file_id}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    fragment_path = os.path.join(directory, f"fragment_{fragment_id}.bin")
    async with aiofiles.open(fragment_path, 'wb') as fragment_file:
        await fragment_file.write(data)


async def process_directory(directory) -> Dict[str, Document]:
    async def calculate_file_hash_and_size(file_path: str) -> Document:
        hash_func = hashlib.md5()
        fragments = 0

        async with aiofiles.open(file_path, 'rb') as file:
            while True:
                data = await file.read(FRAGMENT_SIZE)  # Read in chunks of 1MB
                if not data:
                    break
                hash_func.update(data)
                fragments += 1

        return Document(os.path.basename(file_path), file_path, hash_func.hexdigest(), fragments)

    tasks = []
    for root, dirs, files in os.walk(directory):
        for name in files:
            file_path = os.path.join(root, name)
            tasks.append(calculate_file_hash_and_size(file_path))

    return {result.hash: result for result in await asyncio.gather(*tasks)}


async def get_file_fragment(path: str, fragment_id: int) -> bytes | None:
    if fragment_id <= 0:
        return None
    start_position = (fragment_id - 1) * FRAGMENT_SIZE
    async with aiofiles.open(path, 'rb') as file:
        await file.seek(start_position)
        return await file.read(FRAGMENT_SIZE)
