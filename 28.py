import os
import asyncio
import aiohttp

# Лабораторна робота 28 завдання 1 Коритко Артур

PROJECT_NAME = "async_project"
SUBFOLDERS = ["controllers", "models", "views"]

os.makedirs(PROJECT_NAME, exist_ok=True)
for folder in SUBFOLDERS:
    os.makedirs(os.path.join(PROJECT_NAME, folder), exist_ok=True)

with open(os.path.join(PROJECT_NAME, "requirements.txt"), "w") as f:
    f.write("aiohttp\nasyncio\n")

# Лабораторна робота 28 завдання 2 Коритко Артур


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)

test_urls = [
    "https://jsonplaceholder.typicode.com/todos/1",
    "https://jsonplaceholder.typicode.com/todos/2",
    "https://jsonplaceholder.typicode.com/todos/3",
    "https://jsonplaceholder.typicode.com/todos/4",
    "https://jsonplaceholder.typicode.com/todos/5",
    "https://jsonplaceholder.typicode.com/todos/6",
    "https://jsonplaceholder.typicode.com/todos/7",
    "https://jsonplaceholder.typicode.com/todos/8",
    "https://jsonplaceholder.typicode.com/todos/9",
    "https://jsonplaceholder.typicode.com/todos/10",
]

if __name__ == "__main__":
    responses = asyncio.run(fetch_all(test_urls))
    for i, response in enumerate(responses, 1):
        print(f"Response {i}: {response[:100]}...")
