import asyncio
import logging
import os
import sys

import redis
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from dotenv import load_dotenv

load_dotenv()
# log level
logging.basicConfig(level=logging.INFO)

redis_connect = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), decode_responses=True)

TOKEN = os.getenv('TOKEN')
dp = Dispatcher()


async def wait_and_check(message):
    redis_connect.set(str(message.chat.id), message.text)
    await asyncio.sleep(180)
    if redis_connect.get(str(message.chat.id)) == message.text:
        await message.reply('бля, хорош 🔥')


@dp.message()
async def message_handler(message) -> None:
    await wait_and_check(message)


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
