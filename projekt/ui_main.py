import subprocess
import sys

from client.src.DownloadManager import DownloadManager
from client.src.FileManager import FileManager
from client.src.file_client import FileClient

state = {"connected": False}

file_manager = FileManager("fragments", "../documents")
file_client = FileClient(file_manager)
download_manager = DownloadManager("../documents", file_client, file_manager)


if __name__ == "__main__":
    while True:
        if not state["connected"]:
            user_input = input("Not connected to the network. Please type 'connect' to establish a connection: ")
        else:
            user_input = input("Enter a command (or 'disconnect' to disconnect, 'exit' to quit): ")

        if user_input.lower() == 'exit':
            print("Exiting the loop.")
            break

        if user_input.lower() == 'connect':
            state["connected"] = True
        elif user_input.lower() == 'disconnect':
            state["connected"] = False
        else:
            process = subprocess.run(["python3", "ui_typer.py", user_input], stdout=sys.stdout, text=True)

    print("End of the interaction loop.")



