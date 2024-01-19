import typer
import threading
import time
from tqdm import tqdm


app = typer.Typer()

def long_running_task():
    total = 150
    with tqdm(total=total, desc="Downloading", unit="item", dynamic_ncols=True) as progress_bar:
        for i in range(total):
            time.sleep(0.1)
            progress_bar.update(1)

def run_long_task():
    thread = threading.Thread(target=long_running_task)
    thread.start()

@app.command()
def run_task():
    typer.echo("Running a long task with progress bar:")
    run_long_task()
    typer.echo("Task started in the background.")

@app.command()
def connect(registry="/home/kuba/Documents/sem5/PSI/projekt/23z-psi/projekt/documents", port=6969):
    typer.echo("Connected to the network.")

@app.command()
def disconnect():
    typer.echo("Disconnected from the network.")

@app.command()
def list_files(name: str):
    typer.echo(f"List of files with name '{name}'")

@app.command()
def download_file_fragment(file_hash="b157e8529683a2da7e5e675340a48f6b", fragment_id=1):
    run_long_task()
    typer.echo(f"Downloading file '{file_hash}")

@app.command()
def add_file(file_path: str):
    typer.echo(f"File '{file_path}' added successfully.")

if __name__ == "__main__":
    app()
