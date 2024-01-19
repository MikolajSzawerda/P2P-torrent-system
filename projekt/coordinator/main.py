import logging.config

from src.server_runner import ServerRunner
from src.api import router


logging.config.fileConfig("logging.conf", disable_existing_loggers=False)


def main() -> None:
    api = ServerRunner(router, "127.0.0.1", 65432)
    api.start()


if __name__ == "__main__":
    main()
