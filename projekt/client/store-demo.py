import asyncio
import logging.config

from src.constants import Downloadable

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


async def main():
<<<<<<< HEAD
    results = await process_directory("/home/kuba/Documents/sem5/PSI/projekt/23z-psi/projekt/documents")
    get_file_fragment("/home/kuba/Documents/sem5/PSI/projekt/23z-psi/projekt/documents/example_file.txt",
                      1)
    logger.info("Results %s", results)
=======
    download_queue = {"test": Downloadable("test", "test.txt", 2)}
>>>>>>> 15e6e46be6c827914272a2f2540decac5a507690


if __name__ == '__main__':
    asyncio.run(main())
