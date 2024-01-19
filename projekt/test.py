import typer
import asyncio

app = typer.Typer()

async def async_function():
    await asyncio.sleep(1)
    print("Async function executed")

@app.command()
def async_command():
    asyncio.run(async_function())

@app.command()
def sync_command():
    print("Synchronous function executed")

if __name__ == "__main__":
    app()
