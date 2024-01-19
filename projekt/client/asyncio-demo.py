import asyncio
import logging.config
import sys

from src.file_client import download_fragment
from src.file_server import start_file_sharing
from src.file_store import get_files_registry

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


async def main():
    port = int(sys.argv[1])
    other_port = int(sys.argv[2])
<<<<<<< HEAD
    registry = await process_directory("/home/kuba/Documents/sem5/PSI/projekt/23z-psi/projekt/documents")
    logger.info("Available files: %s", [x.name for x in registry.values()])
=======
    file_registry = await get_files_registry("/home/mszawerd/Studia/SEM5/PSI/proj/23z-psi/projekt/documents")
    logger.info("Available files: %s", [x.name for x in file_registry.values()])
>>>>>>> 15e6e46be6c827914272a2f2540decac5a507690
    if port == 6969:
        await asyncio.gather(
            start_file_sharing(file_registry, port),
            download_fragment("b157e8529683a2da7e5e675340a48f6b", 2, server_port=other_port)
        )
    else:
        await start_file_sharing(file_registry, port)


if __name__ == '__main__':
    asyncio.run(main())
