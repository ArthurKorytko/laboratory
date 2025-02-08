import aiohttp
import asyncio

# Лабораторна робота 25, завдання 1 Коритко Артур


async def fetch(url, session):
    async with session.get(url) as r:
        return await r.json()


async def fetch_all():
    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/2",
        "https://jsonplaceholder.typicode.com/posts/3"
    ]
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(*(fetch(url, session) for url in urls))
    print(results)

# Лабораторна робота 25, завдання 2 Коритко Артур


async def num_generator():
    for i in range(1, 6):
        yield i
        await asyncio.sleep(0.5)


async def print_numbers():
    async for n in num_generator():
        print(n)

# Лабораторна робота 25, завдання 3 Коритко Артур


async def fetch_with_error(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as r:
                r.raise_for_status()
                return await r.json()
    except Exception as e:
        print(f"Error fetching {url}: {e}")


async def main():
    await fetch_all()
    await print_numbers()
    result = await fetch_with_error("https://jsonplaceholder.typicode.com/posts/1")
    if result:
        print(result)

if __name__ == '__main__':
    asyncio.run(main())
