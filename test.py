import asyncio
from telegram import Bot

async def main():
    bot = Bot("8269018717:AAFET4JgFzjAz099wk20agw5JfF69tVNNZw")
    info = await bot.get_me()
    print(info)

asyncio.run(main())
