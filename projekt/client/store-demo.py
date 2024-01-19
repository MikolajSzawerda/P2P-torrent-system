import asyncio
import logging.config

from src.file_store import process_directory, get_file_fragment

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


async def main():
    process_directory("/home/mszawerd/Studia/SEM5/PSI/proj/23z-psi/projekt/documents")
    results = await get_file_fragment("/home/mszawerd/Studia/SEM5/PSI/proj/23z-psi/projekt/documents/example_file.txt",
                                      1)
    logger.info("Results %s", results)


if __name__ == '__main__':
    asyncio.run(main())
