import asyncio
import logging.config

from src.file_store import process_directory, get_file_fragment

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


async def main():
    results = await process_directory("/home/kuba/Documents/sem5/PSI/projekt/23z-psi/projekt/documents")
    get_file_fragment("/home/kuba/Documents/sem5/PSI/projekt/23z-psi/projekt/documents/example_file.txt",
                      1)
    logger.info("Results %s", results)


if __name__ == '__main__':
    asyncio.run(main())
