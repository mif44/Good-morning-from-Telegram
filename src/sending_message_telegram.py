import asyncio
import schedule


from src.weather_request import weather_output
from src.request_exchange_rates import fx_client
from src.random_quote_request import quote_client_ru
from src.good_morning import sends_good_morning
from aiogram.enums import ParseMode
from config import chat_id


async def data_display(bot):
    parts = [
        await weather_output(),
        await fx_client(),
        await quote_client_ru(),
    ]

    text = "\n----------------------------------------------------------------------------------------\n".join(parts)
    good_morning = sends_good_morning()
    await bot.send_message(chat_id, f"<b>{good_morning}</b>", parse_mode=ParseMode.HTML)
    await bot.send_message(chat_id, f"<b>{text}</b>", parse_mode=ParseMode.HTML)


def data_display_job(bot):
    asyncio.create_task(data_display(bot))


async def scheduler(bot):
    schedule.every().day.at("09:00").do(data_display_job, bot)

    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

