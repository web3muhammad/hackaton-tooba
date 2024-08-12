from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

from src.repository import add_user, check_user_exists, get_user_thread
from src.services import create_new_thread
from src.utils import start_gpt

router = Router()


@router.message(CommandStart())
async def answer_start_and_reg(message: Message):
    await message.answer(f"Ассаляму аляйкум, {message.from_user.first_name}, добро пожаловать!")
    if not await check_user_exists(message.from_user.id):
        thread_id = await create_new_thread(message.text)

        await add_user(
            message.from_user.id,
            message.from_user.username,
            message.from_user.full_name,
            thread_id
        )


@router.message(Command("help"))
async def answer_help(message: Message):
    await message.answer(
        ...
    )


@router.message()
async def answer_gpt(message: Message):

    try:
        thread_id = await get_user_thread(message.from_user.id)
        response = await start_gpt(thread_id, message.text)
    except Exception as e:
        print(e)
        await message.answer(f"OpenAI не дает мне вам ответить, "
                             f"пропробуйте позже или обратитесь к моему разработчику")
        return
    try:
        print(response)
        print("SSS", type(message))
        await message.reply(response)
    except Exception:
        await message.answer(f"Telegram не дает мне вам ответить, "
                             f"пропробуйте позже или обратитесь к моему разработчику")
