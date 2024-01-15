from random import choice


class Database:
    def __init__(self):
        self.db = {}

    def add_client(self, client_address, files):
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

