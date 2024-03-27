import pytest
from coordinator.src.statistics import Statistics

@pytest.fixture
def stats():
    return Statistics()

class TestStatistics:
    def test_update_on_connect(self, stats):
        stats.update_on_connect(5)
        assert stats.num_clients == 1
        assert stats.total_visits == 1
        assert stats.total_files_shared == 5
        assert stats.files_per_client == [5]

    def test_update_on_disconnect(self, stats):
        stats.update_on_connect(5)
        stats.update_on_disconnect()
        assert stats.num_clients == 0

    def test_update_shared_files(self, stats):
        stats.update_shared_files(3)
        assert stats.invalid_file_attempts == 3

    def test_update_invalid_files(self, stats):
        stats.update_invalid_files(2)
        assert stats.invalid_file_attempts == 2

    def test_update_on_file_request(self, stats):
        stats.update_on_file_request(4)
        assert stats.total_requested_files == 1
        assert stats.file_owners_quantities == [4]

    def test_generate_report(self, stats):
        stats.update_on_connect(5)
        stats.update_on_disconnect()
        stats.update_shared_files(3)
        stats.update_invalid_files(2)
        stats.update_on_file_request(4)
        report = stats.generate_report()
        assert "Statistics Report:" in report
        assert "Total Visits: 1" in report
        assert "Total Files Shared: 5" in report
        assert "Total Requested Files: 1" in report
        assert "Invalid File Attempts: 5" in report
        assert "Valid/Invalid File Ratio: 1.0" in report
        assert "Average Number of Connected Clients: 0.5" in report
        assert "Average Number of Files per Client: 5.0" in report
        assert "Average Number of File Owners per Requested File: 4.0" in report


    def test_update_on_connect_with_zero_files(self, stats):
        stats.update_on_connect(0)
        assert stats.num_clients == 1
        assert stats.total_visits == 1
        assert stats.total_files_shared == 0
        assert stats.files_per_client == [0]

    def test_update_shared_files_with_zero_files(self, stats):
        stats.update_shared_files(0)
        assert stats.invalid_file_attempts == 0

    def test_update_invalid_files_with_zero_files(self, stats):
        stats.update_invalid_files(0)
        assert stats.invalid_file_attempts == 0

    def test_update_on_file_request_with_zero_owners(self, stats):
        stats.update_on_file_request(0)
        assert stats.total_requested_files == 1
        assert stats.file_owners_quantities == [0]
