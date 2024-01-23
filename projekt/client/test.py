import asyncio


async def main():
    await asyncio.open_connection('192.168.43.9', 8000)


if __name__ == '__main__':
    asyncio.run(main())
