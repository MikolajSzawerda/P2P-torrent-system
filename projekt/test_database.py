import pytest
from Database import Database, FileFormatException


@pytest.fixture
def db():
    db = Database()
    test_data = {
        ("127.0.0.1", "65432"): [
            {"name": "file.txt", "md5": "hdyz", "num_segments": 5, "owned_segments": [0, 1]},
            {"name": "file2.txt", "md5": "hdyz2", "num_segments": 5, "owned_segments": [0, 1, 2]},
        ],
        ("127.0.0.2", "65432"): [
            {"name": "file3.txt", "md5": "hdyz3", "num_segments": 5, "owned_segments": [0, 1]},
            {"name": "file2.txt", "md5": "hdyz2", "num_segments": 5, "owned_segments": [0, 1, 2]},
            {"name": "file4.txt", "md5": "hdyz4", "num_segments": 5, "owned_segments": [0, 1, 2, 3]},
        ],
        ("127.0.0.3", "65432"): [
            {"name": "file5.txt", "md5": "hdyz5", "num_segments": 5, "owned_segments": [0, 1, 2, 3, 4]},
            {"name": "file6.txt", "md5": "hdyz6", "num_segments": 5, "owned_segments": [0, 1, 2, 3, 4]},
        ]
    }
    for client, files in test_data.items():
        db.add_client(client, files)
    return db

def test_add_client(db):
    client = ("127.0.0.2", "65432")
    files = [{"name": "file3.txt", "md5": "hdyz3", "num_segments": 5, "owned_segments": [0, 1]}]
    db.add_client(client, files)
    assert client in db.db

def test_remove_client(db):
    client = ("127.0.0.1", "65432")
    db.remove_client(client)
    assert client not in db.db

def test_get_files_by_name(db):
    files = db.get_files_by_name("file.txt")
    assert len(files) == 1
    assert files[0]['name'] == "file.txt"

def test_get_files_by_md5(db):
    files = db.get_files_by_md5("hdyz")
    assert len(files) == 1
    assert files[0]['md5'] == "hdyz"

def test_get_files_by_name_and_md5(db):
    files = db.get_files_by_name_and_md5("file.txt", "hdyz")
    assert len(files) == 1
    assert files[0]['name'] == "file.txt"
    assert files[0]['md5'] == "hdyz"

def test_get_client_with_file(db):
    client = db.get_client_with_file("file.txt", "hdyz", 0)
    assert client == ("127.0.0.1", "65432")

def test_multiple_clients_with_same_md5(db):
    files = db.get_files_by_md5("hdyz2")
    assert len(files) == 2
    assert all(file['md5'] == "hdyz2" for file in files)

def test_multiple_clients_with_same_name_and_md5(db):
    files = db.get_files_by_name_and_md5("file2.txt", "hdyz2")
    assert len(files) == 2
    assert all(file['name'] == "file2.txt" and file['md5'] == "hdyz2" for file in files)

def test_get_client_with_file_segment(db):
    client = db.get_client_with_file("file5.txt", "hdyz5", 2)
    assert client == ("127.0.0.3", "65432")

def test_get_client_with_non_existent_file_segment(db):
    client = db.get_client_with_file("file.txt", "hdyz", 4)
    assert client is None

def test_verify_files_all_fields_present(db):
    files = [
        {"name": "file.txt", "md5": "hdyz", "num_segments": 5, "owned_segments": [0, 1]},
        {"name": "file2.txt", "md5": "hdyz2", "num_segments": 5, "owned_segments": [0, 1, 2]},
    ]
    db.verify_files(files)  # Should not raise any exception

def test_verify_files_missing_field(db):
    files = [
        {"name": "file.txt", "md5": "hdyz", "num_segments": 5},  # Missing "owned_segments"
    ]
    with pytest.raises(FileFormatException):
        db.verify_files(files)

def test_verify_files_same_name_md5_diff_num_segments(db):
    files = [
        {"name": "file.txt", "md5": "hdyz", "num_segments": 5, "owned_segments": [0, 1]},
    ]
    db.add_client(("127.0.0.1", "65432"), files)
    files = [
        {"name": "file.txt", "md5": "hdyz", "num_segments": 6, "owned_segments": [0, 1]},  # Different "num_segments"
    ]
    with pytest.raises(FileFormatException):
        db.verify_files(files)