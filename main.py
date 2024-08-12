import asyncio
import logging
import os
import sys
from dotenv import load_dotenv
import aiohttp
import io

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InputMediaPhoto
from aiogram.types.bot_command import BotCommand
from aiogram.types import URLInputFile
from aiogram.types import BufferedInputFile

load_dotenv()
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {message.from_user.full_name}! "
                         f"Я - бот присылающий фото и gif котиков. Просто нажми /cat для фото (/10cat для 10 фото)"
                         f" или /cat_gif для gif")


@dp.message(Command(BotCommand(command='cat', description="Get one random photo of cat")))
async def bot_cat(message: Message):
    url: str = 'https://cataas.com/cat'
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        if response.status != 200:
            await message.answer("Что-то пошло не так. Попробуй ещё раз")
        else:
            content = await response.read()
            file = BufferedInputFile(content, filename='image.jpg')
            await message.answer_photo(photo=file)


@dp.message(Command(BotCommand(command='10cat', description="Get ten random photos of cat")))
async def bot_cat_10(message: Message):
    async def get_cat(session, i):
        url: str = 'https://cataas.com/cat'
        response = await session.get(url)
        if response.status != 200:
            return False
        else:
            content = await response.read()
            file = BufferedInputFile(content, filename=f'image{i}.jpg')
            return file

    async with aiohttp.ClientSession() as session:
        tasks = [get_cat(session, i) for i in range(10)]
        res = await asyncio.gather(*tasks)
        files = []
        for f in res:
            if f:
                files.append(InputMediaPhoto(media=f))
        await message.answer_media_group(media=files)


@dp.message(Command(BotCommand(command='cat_gif', description="Get one random gif of cat")))
async def bot_cat_gif(message: Message):
    url: str = 'https://cataas.com/cat/gif'
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        if response.status != 200:
            await message.answer("Что-то пошло не так. Попробуй ещё раз")
        else:
            content = await response.read()
            file = BufferedInputFile(content, filename='image.gif')
            await message.answer_animation(animation=file)


@dp.message(Command(BotCommand(command='help', description="Help")))
async def bot_help(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}! "
                         f"Я - бот присылающий фото и gif котиков. Просто нажми /cat для фото (/10cat для 10 фото)"
                         f" или /cat_gif для gif")


@dp.message()
async def bot_echo(message: Message):
    await message.answer("Вы отправили сообщение:"
                          f"{message.text}. \nЯ не могу разобрать данную команду."
                          f"Воспользуйтесь функцией /help.")


async def main() -> None:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
