from aiogram import Bot, Dispatcher

from src.app.config import settings
from src.app.services import create_new_message, create_new_run, get_response

bot = Bot(token=settings.BOT_TOKEN)

async def start_gpt(thread_id, message_text):
    await create_new_message(thread_id, message_text)
    run = await create_new_run(thread_id)
    return await get_response(thread_id, run)