import typer
from unittest.mock import Mock

app = typer.Typer()

client = Mock()
files_info = []


def check_connection():
    """
    Check if the user is connected to the network.
    """
    connected = True #getattr(client, "connected", False)
    if not connected:
        typer.echo("Not connected to the network. Please connect first.")
    return connected


@app.command()
def connect():
    """
    Connect to the network.
    """
    if not check_connection():
        client.connect_and_send_files.return_value = "success"
        typer.echo("Connected to the network.")
    else:
        typer.echo("Already connected.")


@app.command()
def disconnect():
    """
    Disconnect from the network.
    """
    if check_connection():
        confirm_disconnect = typer.confirm("Are you sure you want to disconnect?")
        if not confirm_disconnect:
            typer.echo("Not disconnecting.")
            raise typer.Abort()
        client.connected = False
        typer.echo("Disconnected from the network.")


@app.command()
def list_files(name: str):
    """
    List available files.
    """
    if check_connection():
        client.search_by_name.return_value = [
            {"name": name, "md5": "12345", "num_segments": 5, "owned_segments": [0, 1, 3]},
            {"name": name, "md5": "12346", "num_segments": 5, "owned_segments": [0, 1, 2, 3, 4]}
        ]
        typer.echo(f"List of files with name '{name}': {client.search_by_name.return_value}")


@app.command()
def download_file(name: str, md5: str):
    """
    Download a file.
    """
    if check_connection():
        client.search_by_name_and_md5.return_value = {"name": name, "md5": md5, "num_segments": 5, "owned_segments": [0, 1, 3]}
        typer.echo(f"Downloading file '{name}' with MD5 '{md5}'")


@app.command()
def add_file(file_path: str):
    """
    Add a file to the network.
    """
    if check_connection():
        client.calculate_md5.return_value = "abcde"
        client.update_client.return_value = "success"
        files_info.append({"name": file_path, "md5": "abcde", "num_segments": 5, "owned_segments": [0, 1, 2, 3, 4]})
        typer.echo(f"File '{file_path}' added successfully.")


if __name__ == "__main__":
    app()
