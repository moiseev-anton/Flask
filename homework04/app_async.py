import asyncio
import aiofiles
import aiohttp
import argparse
import time


async def download_image(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.read()
                return data


async def save_image(data, filename):
    async with aiofiles.open(filename, "wb") as f:
        await f.write(data)
        print(f"Image saved as {filename}")


async def process_url(url, index):
    start_time = time.time()
    data = await download_image(url)
    if data:
        extension = url.split('.')[-1]
        filename = f"images/image{index}.{extension}"
        await save_image(data, filename)
        print(f"{index}: {time.time() - start_time:.2f} seconds")


async def main(urls):
    start_time = time.time()
    tasks = []
    for i, url in enumerate(urls, start=1):
        task = asyncio.create_task(process_url(url, i))
        tasks.append(task)
    await asyncio.gather(*tasks)
    print(f"Total time: {time.time() - start_time:.2f} ")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download images from URLs")
    parser.add_argument("urls", metavar="url", type=str, nargs="*", help="URLs of images to download")
    args = parser.parse_args()

    asyncio.run(main(args.urls))
