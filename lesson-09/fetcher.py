import asyncio
import aiohttp


URL = "https://docs.python.org/3/whatsnew/3.14.html"


async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.text()
            return data


async def fetch_batch_urls(urls):
    tasks = []
    for url in urls:
        tasks.append(fetch_url(url))

    results = await asyncio.gather(*tasks)
    print(
        "fetch_batch_urls",
        len(results),
        [len(res) for res in results]
    )

    return results


if __name__ == "__main__":
    asyncio.run(fetch_batch_urls([URL] * 10))
