import pytest
from coordinator.src.coordinator import Coordinator
import logging
from coordinator.src.schema import File, FileId
from coordinator.src.statistics import Statistics

logger = logging.getLogger(__name__)


@pytest.fixture
def coordinator():
    stats = Statistics()
    return Coordinator(stats)


class TestCoordinatorStatisticsIntegration:
    def test_connect_client_updates_statistics(self, coordinator):
        coordinator.connect_client("client1", [])
        assert coordinator._statistics.num_clients == 1
        assert coordinator._statistics.total_visits == 1

    def test_disconnect_client_updates_statistics(self, coordinator):
        coordinator.connect_client("client1", [])
        coordinator.disconnect_client("client1")
        assert coordinator._statistics.num_clients == 0

    def test_share_file_updates_statistics(self, coordinator):
        file = File(FileId("file1", "client1"), 10)
        coordinator.connect_client("client1", [file])
        coordinator.share_file("client1", file)
        assert coordinator._statistics.total_files_shared == 1

    def test_invalid_file_updates_statistics(self, coordinator):
        file = File(FileId("file1", "client1"), 10)
        invalid_file = File(FileId("file1", "client2"), 10)
        coordinator.connect_client("client1", [file])
        coordinator.share_file("client1", invalid_file)
        assert coordinator._statistics.invalid_file_attempts == 1

    def test_assign_segments_updates_statistics(self, coordinator):
        file = File(FileId("file1", "client1"), 10)
        coordinator.connect_client("client1", [file])
        a=  coordinator.assign_segments(file.id, [0])
        assert coordinator._statistics.total_requested_files == 1
        assert coordinator._statistics.file_owners_quantities == [1]
