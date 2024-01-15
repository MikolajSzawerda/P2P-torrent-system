import pytest
from Database import Database


@pytest.fixture
def db():
    db = Database()
    test_data = {
        ("127.0.0.1", "65432"): [
            {"name": "file.txt", "md5": "hdyż", "num_segments": 5, "owned_segments": [0, 1]},
            {"name": "file2.txt", "md5": "hdyż2", "num_segments": 5, "owned_segments": [0, 1, 2]},
        ],
        ("127.0.0.2", "65432"): [
            {"name": "file3.txt", "md5": "hdyż3", "num_segments": 5, "owned_segments": [0, 1]},
            {"name": "file2.txt", "md5": "hdyż2", "num_segments": 5, "owned_segments": [0, 1, 2]},
            {"name": "file4.txt", "md5": "hdyż4", "num_segments": 5, "owned_segments": [0, 1, 2, 3]},
        ],
        ("127.0.0.3", "65432"): [
            {"name": "file5.txt", "md5": "hdyż5", "num_segments": 5, "owned_segments": [0, 1, 2, 3, 4]},
            {"name": "file6.txt", "md5": "hdyż6", "num_segments": 5, "owned_segments": [0, 1, 2, 3, 4]},
        ]
    }
    for client, files in test_data.items():
        db.add_client(client, files)
    return db

def test_add_client(db):
    client = ("127.0.0.2", "65432")
    files = [{"name": "file3.txt", "md5": "hdyż3", "num_segments": 5, "owned_segments": [0, 1]}]
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
    files = db.get_files_by_md5("hdyż")
    assert len(files) == 1
    assert files[0]['md5'] == "hdyż"

def test_get_files_by_name_and_md5(db):
    files = db.get_files_by_name_and_md5("file.txt", "hdyż")
    assert len(files) == 1
    assert files[0]['name'] == "file.txt"
    assert files[0]['md5'] == "hdyż"

def test_get_client_with_file(db):
    client = db.get_client_with_file("file.txt", "hdyż", 0)
    assert client == ("127.0.0.1", "65432")

def test_multiple_clients_with_same_md5(db):
    files = db.get_files_by_md5("hdyż2")
    assert len(files) == 2
    assert all(file['md5'] == "hdyż2" for file in files)

def test_multiple_clients_with_same_name_and_md5(db):
    files = db.get_files_by_name_and_md5("file2.txt", "hdyż2")
    assert len(files) == 2
    assert all(file['name'] == "file2.txt" and file['md5'] == "hdyż2" for file in files)

def test_get_client_with_file_segment(db):
    client = db.get_client_with_file("file5.txt", "hdyż5", 2)
    assert client == ("127.0.0.3", "65432")

def test_get_client_with_non_existent_file_segment(db):
    client = db.get_client_with_file("file.txt", "hdyż", 4)
    assert client is None