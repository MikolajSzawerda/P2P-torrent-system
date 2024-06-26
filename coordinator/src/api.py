import logging

from .connected_client import ConnectedClient
from .coordinator import Coordinator
from .routes_registry import RoutesRegistry
from .schema import FileId, File

logger = logging.getLogger(__name__)

router = RoutesRegistry()
coordinator = Coordinator()


@router.register("connect")
async def connect_client(client: ConnectedClient, server_port: int, files: list[dict]) -> None:
    logger.info("Connecting client %s with %s files and server port %s", client.id, len(files), server_port)

    coordinator.connect_client(client.id, [File.from_dict(file) for file in files], server_port)
    await client.send_success_response()


@router.register("share_file")
async def share_file(client: ConnectedClient, file: dict) -> None:
    logger.info("Client %s has shared a new file %s", client.id, file)

    coordinator.share_file(client.id, File.from_dict(file))
    await client.send_success_response()


@router.register("disconnect")
async def disconnect_client(client: ConnectedClient) -> None:
    logger.info("Disconnecting client %s", client.id)

    coordinator.disconnect_client(client.id)
    await client.disconnect()


@router.register("search_by_name")
async def search_files_by_name(client: ConnectedClient, name: str) -> None:
    logger.info("Client %s is searching for file %s", client.id, name)

    result = coordinator.search_by_name(name)
    await client.send([file.asdict() for file in result])


@router.register("assign_segments")
async def assign_segments(
        client: ConnectedClient, name: str, hash: str, segment_ids: list[int]
) -> None:
    logger.info(
        "Client %s is requesting an assignment of %s segments for file %s",
        client.id,
        len(segment_ids),
        name,
    )

    assignment = coordinator.assign_segments(FileId(name, hash), segment_ids)
    logger.info("Assignment for file %s received %s", name, assignment)

    await client.send(assignment)

@router.register("generate_stats")
async def generate_stats(client: ConnectedClient) -> None:
    stats_report = coordinator.generate_stats()
    logger.info("Statistics stats_report generated: %s", stats_report)

    await client.send(stats_report)
