from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from handlers import register_handlers

import asyncio
import os

async def start() -> None:
    token = os.getenv("TELEGRAM_TOKEN")
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()
    register_handlers(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(start())