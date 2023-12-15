import asyncio
import logging
import os
import sys
import requests
import json
import redis
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from dotenv import load_dotenv

# log level
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logging.info(f"Loading ENV")
load_dotenv()

logging.info(f"Connecting to Redis")
redis_connect = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), decode_responses=True)

TOKEN = os.getenv('TOKEN')
dp = Dispatcher()

tasks = {}


def get_random_answer():
    #get answer from open API
    url = "https://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        answer = json.loads(response.text)
        return answer.get("quoteText", "бля, хорош 🔥")
    return "бля, хорош 🔥"


async def wait_and_check(message):
    # write data to redis
    logging.info("Set data in Redis")
    redis_connect.set(message.chat.id, message.message_id)
    await asyncio.sleep(600)
    # check if data updated after time
    if redis_connect.get(message.chat.id) == str(message.message_id):
        await message.reply(get_random_answer())


@dp.message()
async def message_handler(message) -> None:
    logging.info(f"Got a message from the chat: {message.chat.id}")
    if (task := tasks.get(message.chat.id)) and not task.done():
        task.cancel()
    logging.info(f"Creating a task and saving the task in the memory")
    tasks[message.chat.id] = asyncio.create_task(wait_and_check(message))
    await tasks[message.chat.id]


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    logging.info(f"Initializing TheyWillTextYou_BOT ")
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    logging.info(f"Starting polling")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
