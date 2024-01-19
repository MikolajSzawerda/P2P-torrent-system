import logging.config

from src.server_runner import ServerRunner
from src.api import router


logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

HOST = "127.0.0.1"
PORT = 65432


def main() -> None:
    api = ServerRunner(router, HOST, PORT)
    api.start()


if __name__ == "__main__":
    main()
