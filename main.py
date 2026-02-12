import asyncio

from src.sending_message_telegram import data_display
from aiogram import Bot, Dispatcher
from config import bot_token


bot = Bot(token=bot_token)


async def main():
    try:
        await data_display(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())