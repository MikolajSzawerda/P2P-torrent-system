class Statistics:
    def __init__(self):
        self.total_visits = 0
        self.total_files_shared = 0
        self.total_requested_files = 0
        self.invalid_file_attempts = 0

        self.num_clients = 0
        self.files_per_client = []
        self.file_owners_quantities = []

        self.quantity_of_connected_clients = []

    def update_on_connect(self, num_files_shared: int):
        self.num_clients += 1
        self.quantity_of_connected_clients.append(self.num_clients)

        self.total_visits += 1
        self.total_files_shared += num_files_shared
        self.files_per_client.append(num_files_shared)


    def update_on_disconnect(self):
        self.num_clients -= 1
        self.quantity_of_connected_clients.append(self.num_clients)

    def update_shared_files(self, number: int):
        self.invalid_file_attempts += number

    def update_invalid_files(self, number: int):
        self.invalid_file_attempts += number

    def update_on_file_request(self, num_file_owners: int):
        self.total_requested_files += 1
        self.file_owners_quantities.append(num_file_owners)

    def generate_report(self):
        report = "Statistics Report:\n"
        report += f"Total Visits: {self.total_visits}\n"
        report += f"Total Files Shared: {self.total_files_shared}\n"
        report += f"Total Requested Files: {self.total_requested_files}\n"
        report += f"Invalid File Attempts: {self.invalid_file_attempts}\n"
        report += f"Valid/Invalid File Ratio: {self._calculate_ratio(self.total_files_shared, self.invalid_file_attempts)}\n"
        report += f"Average Number of Connected Clients: {self._calculate_average(self.quantity_of_connected_clients)}\n"
        report += f"Average Number of Files per Client: {self._calculate_average(self.files_per_client)}\n"
        report += f"Average Number of File Owners per Requested File: {self._calculate_average(self.file_owners_quantities)}\n"
        return report

    def _calculate_average(self, data_list):
        return sum(data_list) / len(data_list) if data_list else 0

    def _calculate_ratio(self, valid, invalid):
        return valid / invalid if invalid else float("inf")
