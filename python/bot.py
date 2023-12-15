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
import g4f

# log level
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logging.info(f"Loading ENV")
load_dotenv()

logging.info(f"Connecting to Redis")
redis_connect = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), decode_responses=True, db=0)

TOKEN = os.getenv('TOKEN')
dp = Dispatcher()

tasks = {}

_providers = [
    g4f.Provider.FreeGpt,
    g4f.Provider.You,
    g4f.Provider.GeekGpt,
    g4f.Provider.FakeGpt,
    g4f.Provider.Berlin,
    g4f.Provider.Koala,
    g4f.Provider.Chatgpt4Online,
    g4f.Provider.ChatAnywhere,
    g4f.Provider.ChatgptDemoAi,
    # g4f.Provider.OnlineGpt,
    g4f.Provider.ChatgptNext,
]


def get_random_answer():
    # get answer from open API
    url = "https://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        answer = json.loads(response.text)
        return answer.get("quoteText", "бля, хорош 🔥")
    return "бля, хорош 🔥"


async def get_gpt_answer(message):
    for provider in _providers:
        try:
            response = await g4f.ChatCompletion.create_async(
                model=g4f.models.gpt_35_long,
                messages=[{"role": "user",
                           "content": f"Скажи по этом поводу что-то одним предложением в стиле быдло, гопника или необразованного человека: {message.text}"}],
                provider=provider
            )
            logging.info('Успешный запрос к {}'.format(str(provider)))
            return await message.reply(response)
        except:
            logging.error('Ошибка запроса к {}'.format(str(provider)))
    return await message.reply(get_random_answer())


async def wait_and_check(message):
    # write data to redis
    logging.info("Set data in Redis")
    redis_connect.set(str(message.chat.id), message.message_id)
    await asyncio.sleep(360)
    # check if data updated after time
    if redis_connect.get(str(message.chat.id)) == str(message.message_id):
        await get_gpt_answer(message)


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
