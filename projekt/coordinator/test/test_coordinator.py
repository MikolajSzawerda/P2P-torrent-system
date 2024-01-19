import pytest

from coordinator.src.schema import File, FileId


def test_client_cant_connect_twice(coordinator):
    coordinator.connect_client("123", [])

    with pytest.raises(ValueError):
        coordinator.connect_client("123", [])


def test_file_can_be_found_by_name_after_client_shared_when_connecting(coordinator):
    file1 = File(id=FileId(name="a.txt", hash="a12"), size=123)
    file2 = File(id=FileId(name="b.txt", hash="b12"), size=123)
    file3 = File(id=FileId(name="a.txt", hash="other_hash"), size=456)

    coordinator.connect_client("123", [file1, file2])
    coordinator.connect_client("456", [file3])

    assert coordinator.search_by_name("a.txt") == [file1, file3]


def test_file_still_can_be_found_by_name_when_not_all_owners_disconnected(coordinator):
    file = File(id=FileId(name="a.txt", hash="a12"), size=12)

    coordinator.connect_client("1", [file])
    coordinator.connect_client("2", [file])
    coordinator.connect_client("3", [file])

    coordinator.disconnect_client("1")

    assert coordinator.search_by_name("a.txt") == [file]


def test_file_cant_be_found_by_name_when_all_owners_disconnected(coordinator):
    file = File(id=FileId(name="a.txt", hash="a12"), size=12)

    coordinator.connect_client("1", [file])
    coordinator.connect_client("2", [file])
    coordinator.connect_client("3", [file])

    coordinator.disconnect_client("1")
    coordinator.disconnect_client("2")
    coordinator.disconnect_client("3")

    assert coordinator.search_by_name("a.txt") == []


def test_client_cant_disconnect_when_not_connected(coordinator):
    with pytest.raises(ValueError):
        coordinator.disconnect_client("123")


def test_file_can_be_shared_after_connecting(coordinator):
    file = File(id=FileId(name="a.txt", hash="a12"), size=12)

    coordinator.connect_client("1", [])
    coordinator.share_file("1", file)

    assert coordinator.search_by_name("a.txt") == [file]


def test_should_assign_file_segments_evenly(coordinator):
    file_id = FileId(name="a.txt", hash="a12")
    file = File(id=file_id, size=File.SEGMENT_SIZE_BYTES * 4)

    coordinator.connect_client("1", [file])
    coordinator.connect_client("2", [file])
    coordinator.connect_client("3", [file])

    assert coordinator.assign_segments(file_id, [0, 1, 2, 3]) == {
        0: "1",
        1: "2",
        2: "3",
        3: "1",
    }


def test_should_make_partial_segments_assignment(coordinator):
    file_id = FileId(name="a.txt", hash="a12")
    file = File(id=file_id, size=File.SEGMENT_SIZE_BYTES * 4)

    coordinator.connect_client("1", [file])

    assert coordinator.assign_segments(file_id, [0, 3]) == {
        0: "1",
        3: "1",
    }


def test_should_not_assign_file_when_invalid_segments_are_passed(coordinator):
    file_id = FileId(name="a.txt", hash="a12")
    file = File(id=file_id, size=File.SEGMENT_SIZE_BYTES * 4)

    coordinator.connect_client("1", [file])

    assert coordinator.assign_segments(file_id, [-1]) == {}
    assert coordinator.assign_segments(file_id, [4]) == {}


def test_should_not_assign_file_when_it_doesnt_exist_anymore(coordinator):
    file_id = FileId(name="a.txt", hash="a12")
    file = File(id=file_id, size=File.SEGMENT_SIZE_BYTES * 4)

    coordinator.connect_client("1", [file])
    coordinator.disconnect_client("1")

    assert coordinator.assign_segments(file_id, [1]) == {}
