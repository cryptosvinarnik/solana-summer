import aiohttp
import asyncio

from loguru import logger


url = "https://solana.us17.list-manage.com/subscribe/" \
      "post-json?u=dc5b8a6eb6dc3d737579c03c9&" \
      "id=a43a9eb2ad&EMAIL={}&c=__jp0"


async def subscribe_on_solana(worker: str, queue: asyncio.Queue) -> bool:
    i = 0

    while True:
        email = await queue.get()

        async with aiohttp.ClientSession() as session:
            async with session.get(url.format(email)) as resp:
                if "Thank" in await resp.text():
                    logger.success(
                        f"{worker} - {email} successfully registered")
                else:
                    logger.error(f"{worker} - {email} - error!")

        i += 1

        if i % 4 == 0:
            logger.info("Sleeping 60 seconds...")
            await asyncio.sleep(60)

        if queue.empty():
            return True


async def main(emails):
    queue = asyncio.Queue()

    for email in emails:
        queue.put_nowait(email)

    tasks = [asyncio.create_task(subscribe_on_solana(
             f"Worker {i}", queue)) for i in range(5)]

    await asyncio.gather(*tasks)

