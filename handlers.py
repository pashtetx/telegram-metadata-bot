from aiogram import Dispatcher, Bot, F
from aiogram.filters.command import CommandStart
from aiogram.types import Message
from analyzer import parse_image

async def start(message: Message) -> None:
    response = (
        "Привет! 👋 Я бот для того чтобы узнать гео локацию по фотографии! 🕵️",
        "",
        "🤔  Для того чтобы узнать геолокацию, нужно фотографию отправить как файл!",
        "",
        "⛔  <i>Бот может не узнать геолокацию если у жертвы для камеры не разрешена геолокация!</i>",
        "⚙️  <i>Разработчик: @migainis</i>"
    )
    await message.answer("\n".join(response))

async def capture_photo(message: Message, bot: Bot) -> None:
    file_id = message.document.file_id
    image = await bot.download(file_id)
    response = parse_image(image, filename=message.document.file_name)
    await message.answer("\n".join(response))

def register_handlers(dp: Dispatcher) -> None:
    dp.message.register(start, CommandStart())
    dp.message.register(capture_photo, F.document)