import typer
import asyncio

from client.src.file_server import start_file_sharing
from client.src.file_client import download_fragment


app = typer.Typer()

@app.command()
def connect(registry="/home/kuba/Documents/sem5/PSI/projekt/23z-psi/projekt/documents", port=6969):
    asyncio.run(start_file_sharing(registry, port)),
    typer.echo("Connected to the network.")

@app.command()
def disconnect():
    typer.echo("Disconnected from the network.")

@app.command()
def list_files(name: str):
    typer.echo(f"List of files with name '{name}'")

@app.command()
def download_file_fragment(file_hash="b157e8529683a2da7e5e675340a48f6b", fragment_id=1):
    asyncio.run(download_fragment(file_hash, fragment_id))
    typer.echo(f"Downloading file '{file_hash}")

@app.command()
def add_file(file_path: str):
    typer.echo(f"File '{file_path}' added successfully.")

if __name__ == "__main__":
    app()
