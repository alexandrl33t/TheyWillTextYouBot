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

tasks = {}


async def wait_and_check(message):
    # write data to redis
    redis_connect.set(message.chat.id, message.message_id)
    await asyncio.sleep(10)
    if redis_connect.get(message.chat.id) == str(message.message_id):
        await message.reply('бля, хорош 🔥')


@dp.message()
async def message_handler(message) -> None:
    if task := tasks.get(message.chat.id):
        task.cancel()
    tasks[message.chat.id] = asyncio.create_task(wait_and_check(message))
    await tasks[message.chat.id]


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
