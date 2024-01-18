from random import choice

class FileFormatException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class Database:
    def __init__(self):
        self.db = {}

    def verify_files(self, files):
        for file in files:
            # Check if file has all required fields
            if not all(key in file for key in ["name", "md5", "num_segments", "owned_segments"]):
                print(file)
                raise FileFormatException("File does not have all required fields")

            # Check if file with same name and md5 but different num_segments exists in the database
            existing_files = self.get_files_by_name_and_md5(file['name'], file['md5'])
            if any(existing_file['num_segments'] != file['num_segments'] for existing_file in existing_files):
                raise FileFormatException("File with same name and md5 but different num_segments exists in the database")

    def add_client(self, client_address, files):
        self.verify_files(files)
        self.db[client_address] = files

    def remove_client(self, client_address):
        if client_address in self.db:
            del self.db[client_address]

    def get_files_by_name(self, name):
        result = []
        for client in self.db.values():
            result.extend([file for file in client if file['name'] == name])
        return result

    def get_files_by_md5(self, md5):
        result = []
        for client in self.db.values():
            result.extend([file for file in client if file['md5'] == md5])
        return result

    def get_files_by_name_and_md5(self, name, md5):
        result = []
        for client in self.db.values():
            result.extend([file for file in client if file['name'] == name and file['md5'] == md5])
        return result

    def get_client_with_file(self, name, md5, segment_number):
        clients = []
        for client_address, files in self.db.items():
            for file in files:
                if file['name'] == name and file['md5'] == md5 and segment_number in file['owned_segments']:
                    clients.append(client_address)
        if len(clients) != 0:
            return choice(clients)
        return None

    def get_all_data(self):
        """
        debug only method
        :return:
        """
        return self.db
