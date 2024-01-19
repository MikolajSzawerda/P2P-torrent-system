import asyncio
import logging.config
import sys

from src.file_client import download_fragment
from src.file_server import start_file_sharing

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)


async def main():
    port = int(sys.argv[1])
    other_port = int(sys.argv[2])
    if port == 6969:
        await asyncio.gather(
            start_file_sharing(port),
            download_fragment(server_port=other_port)
        )
    else:
        await start_file_sharing(port)


if __name__ == '__main__':
    asyncio.run(main())
