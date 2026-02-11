import asyncio

from src.sending_message_telegram import scheduler
from aiogram import Bot, Dispatcher
from config import bot_token


bot = Bot(token=bot_token)
dp = Dispatcher()


async def main():
    asyncio.create_task(scheduler(bot))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())