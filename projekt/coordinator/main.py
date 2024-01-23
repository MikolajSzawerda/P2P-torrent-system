import logging.config

from src.api import router
from src.server_runner import ServerRunner

logging.config.fileConfig("./coordinator/logging.conf", disable_existing_loggers=False)

HOST = "0.0.0.0"
PORT = 65432


def main() -> None:
    api = ServerRunner(router, HOST, PORT)
    api.start()


if __name__ == "__main__":
    main()
