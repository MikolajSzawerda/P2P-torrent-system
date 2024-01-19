import logging

from coordinator.src.connected_client import ConnectedClient
from coordinator.src.coordinator import Coordinator
from coordinator.src.repository import Repository
from coordinator.src.routes_registry import RoutesRegistry
from coordinator.src.schema import FileId

logger = logging.getLogger(__name__)

router = RoutesRegistry()

repository = Repository()

coordinator = Coordinator(repository)


@router.register("connect")
async def connect_client(client: ConnectedClient) -> None:
    logger.info("Connecting client")
    coordinator.connect_client(client)


@router.register("disconnect")
async def disconnect_client(client: ConnectedClient) -> None:
    logger.info("Disconnecting client")
    coordinator.disconnect_client(client)
    await client.disconnect()


@router.register("search_by_name")
async def search_files_by_name(client: ConnectedClient, name: str) -> None:
    res = coordinator.search_by_name(name)
    await client.send(res)


@router.register("find_segments")
async def assign_segments(
    client: ConnectedClient, name: str, md5: str, segment_ids: list[int]
) -> None:
    assignment = coordinator.assign_segments(FileId(name, md5), segment_ids)
    await client.send(assignment)
