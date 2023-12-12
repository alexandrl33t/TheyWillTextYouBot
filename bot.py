import sys

from aiogram.enums import ParseMode
import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, Router, types
from dotenv import load_dotenv

load_dotenv()
# log level
logging.basicConfig(level=logging.INFO)

token = os.getenv('TOKEN')

dp = Dispatcher()

last_message = None



@dp.message()
async def echo_handler(message) -> None:
    if message.chat.id == -1001828812929:
        logging.info('все ок')
    else:
        if message.reply_to_message:
            logging.info(message)
        last_message = message.model_copy()
        logging.info('gjdsadsadsa')
        await message.answer('бля, хорош 🔥')


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(token, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
