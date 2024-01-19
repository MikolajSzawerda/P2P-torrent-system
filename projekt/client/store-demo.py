import asyncio
import logging.config

from src.constants import Downloadable

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


async def main():
    download_queue = {"test": Downloadable("test", "test.txt", 2)}


if __name__ == '__main__':
    asyncio.run(main())
