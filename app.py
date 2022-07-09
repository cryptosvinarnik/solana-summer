import asyncio

from solana import main


if __name__ == "__main__":
    with open(input("Filename with emails: ")) as file:
        emails = file.read().splitlines()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(main(emails))