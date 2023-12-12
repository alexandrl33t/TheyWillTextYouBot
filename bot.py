import sys

from aiogram.enums import ParseMode
import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, Router, types
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.schedulers.background import BlockingScheduler
from dotenv import load_dotenv

load_dotenv()
# log level
logging.basicConfig(level=logging.INFO)


TOKEN = os.getenv('TOKEN')
REDIS_URL = os.getenv('REDIS_URL')
storage = RedisStorage.from_url(REDIS_URL)
dp = Dispatcher(storage=storage)


async def wait_and_check(message):
    await dp.storage.set_state('message_id', message.id)
    await asyncio.sleep(5)
    await dp.storage.get_state('message_id')
    await message.reply('бля, хорош 🔥')


@dp.message()
async def message_handler(message) -> None:
    if message.chat.id == -1001828812929:
        logging.info('все ок')
    else:
        if message.reply_to_message:
            logging.info(message)
        last_message = message.model_copy()
        await wait_and_check(message)


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
