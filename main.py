import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.filters.command import Command
from aiogram.types import Message
from dotenv import load_dotenv, find_dotenv

from src.code import get_code


load_dotenv(find_dotenv(usecwd=True))


TOKEN = getenv("TELEGRAM_BOT_TOKEN")
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
  await message.answer(
    f"Hello, *{message.from_user.full_name}*!", parse_mode=ParseMode.MARKDOWN
  )


@dp.message(Command('code'))
async def code(message: Message) -> None:
  chat = message.chat
  msg = message.reply_to_message

  if not msg:
    await message.reply('Reply to the message')
  if not msg.text:
    await message.reply('Reply message no text')

  try:
    await chat.delete_message(message.message_id)
  except Exception:
    pass

  await msg.reply(get_code(msg.text.strip()))


async def main() -> None:
  bot = Bot(
    token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
  )
  await dp.start_polling(bot)


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO, stream=sys.stdout)
  asyncio.run(main())
