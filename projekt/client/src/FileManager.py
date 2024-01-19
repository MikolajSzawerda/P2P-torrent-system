import asyncio
import hashlib
import logging.config
import os
from typing import Dict

import aiofiles

from .constants import FragmentedDocument, Document, FRAGMENT_SIZE
from .file_store import get_fragments_registry

logger = logging.getLogger(__name__)


class FileManager:
    def __init__(self, fragments_path: str, documents_path: str):
        self.fragments_path = fragments_path
        self.documents_path = documents_path
        self._fragments_registry: Dict[str, FragmentedDocument] = get_fragments_registry(fragments_path)
        self._files_registry = {}

    async def merge_fragments(self, file_hash, file_name):
        file_dir = self._fragments_registry[file_hash].path
        files = sorted(os.listdir(file_dir))
        output_name = os.path.join(self.documents_path, file_name)
        async with aiofiles.open(output_name, 'wb') as outfile:
            for filename in files:
                if os.path.isfile(os.path.join(file_dir, filename)):
                    async with aiofiles.open(os.path.join(file_dir, filename), 'rb') as infile:
                        content = await infile.read()
                        await outfile.write(content)

    def add_document(self, file_hash, num_of_fragments: int):
        path = os.path.join(self.fragments_path, file_hash)
        if not os.path.exists(path):
            os.mkdir(path)
        self._fragments_registry[file_hash] = FragmentedDocument(file_hash, path, set(), num_of_fragments)

    def get_missing_file_fragments(self, file_hash):
        return self._fragments_registry[file_hash].get_missing_fragments()

    async def add_fragment(self, file_hash, fragment_id, data):
        path = os.path.join(self.fragments_path, file_hash)
        if not os.path.exists(path):
            os.makedirs(path)

        fragment_path = os.path.join(path, f"fragment_{fragment_id}.bin")
        async with aiofiles.open(fragment_path, 'wb') as fragment_file:
            await fragment_file.write(data)
        self._fragments_registry[file_hash].current_fragments.add(fragment_id)

    async def get_files_registry(self) -> Dict[str, Document]:
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

            return Document(os.path.basename(file_path), file_path, hash_func.hexdigest(), fragments,
                            os.stat(file_path).st_size)

        tasks = []
        for root, dirs, files in os.walk(self.documents_path):
            for name in files:
                file_path = os.path.join(root, name)
                tasks.append(calculate_file_hash_and_size(file_path))
        res = {result.hash: result for result in await asyncio.gather(*tasks)}
        self._files_registry = res
        return res

    def get_files_as_dict(self):
        return [{
            'name': x.name,
            'hash': x.hash,
            'size': x.size
        } for x in self._files_registry.values()]
