import asyncio
import hashlib
import logging
import os
import re
from typing import Dict

import aiofiles

from .constants import FRAGMENT_SIZE, Document, FragmentedDocument

logger = logging.getLogger(__name__)


async def save_fragment(file_id, fragment_id, data):
    directory = f"fragments/{file_id}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    fragment_path = os.path.join(directory, f"fragment_{fragment_id}.bin")
    async with aiofiles.open(fragment_path, 'wb') as fragment_file:
        await fragment_file.write(data)


async def get_files_registry(directory) -> Dict[str, Document]:
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

        return Document(os.path.basename(file_path), file_path, hash_func.hexdigest(), fragments, 160)

    tasks = []
    for root, dirs, files in os.walk(directory):
        for name in files:
            file_path = os.path.join(root, name)
            tasks.append(calculate_file_hash_and_size(file_path))

    return {result.hash: result for result in await asyncio.gather(*tasks)}


def get_fragments_registry(parent_directory) -> Dict[str, FragmentedDocument]:
    def extract_frag_id(filename):
        match = re.search(r'fragment_(\d+).bin', filename)
        if match:
            return int(match.group(1))
        else:
            return None

    registry = {}
    for name in os.listdir(parent_directory):
        subdirectory = os.path.join(parent_directory, name)
        if os.path.isdir(subdirectory):
            fragments = {extract_frag_id(file) for file in os.listdir(subdirectory)
                         if os.path.isfile(os.path.join(subdirectory, file))}
            registry[name] = FragmentedDocument(name, subdirectory, fragments, 2)
    return registry


async def get_file_fragment(path: str, fragment_id: int) -> bytes | None:
    if fragment_id <= 0:
        return None
    start_position = (fragment_id - 1) * FRAGMENT_SIZE
    async with aiofiles.open(path, 'rb') as file:
        await file.seek(start_position)
        return await file.read(FRAGMENT_SIZE)
