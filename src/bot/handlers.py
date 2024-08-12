from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

from src.bot.keyboards import inline_kb, web_kb
from src.repository import add_user, check_user_exists, get_user_thread
from src.services import create_new_thread
from src.utils import start_gpt

router = Router()


@router.message(CommandStart())
async def answer_start_and_reg(message: Message):
    await message.answer(f"Ассаляму аляйкум, {message.from_user.first_name}, в чем мои преимущества?\n\n"
                         f"- Анализ интересов пользователя для подбора проектов, "
                         f"которые соответствуют его увлечениям и ценностям.\n"
                         f"- Обеспечение возможности делать пожертвования прямо через интерфейс чата\n"
                         f"- Предложение подходящих сумм пожертвований, учитывая финансовое положение пользователя\n"
                         f"- Предоставление детальной информации о том, "
                         f"как распределяются пожертвования и какое влияние они оказывают\n"
                         f"- Общение с пользователями в дружеской и поддерживающей манере, создавая атмосферу доверия\n"
                         f"- Использование убедительных методов коммуникации для мотивации к пожертвованиям, "
                         f"подчеркивая их важность и влияние\n"
                         f"- Сбор отзывов от пользователей для постоянного улучшения качества "
                         f"обслуживания и удовлетворенности пользователей\n"
                         f"\n"
                         f"Основная цель — сделать приложение Tooba интуитивно понятным, дружественным и "
                         f"эффективным инструментом для максимального увеличения влияния благотворительных пожертвований.",
                         reply_markup=web_kb)
    if not await check_user_exists(message.from_user.id):
        thread_id = await create_new_thread(message.text)

        await add_user(
            message.from_user.id,
            message.from_user.username,
            message.from_user.full_name,
            thread_id
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
        if response.__contains__(":)"):
            await message.reply(response, reply_markup=inline_kb)
        else:
            await message.reply(response)
    except Exception:
        await message.answer(f"Telegram не дает мне вам ответить, "
                             f"пропробуйте позже или обратитесь к моему разработчику")


@router.callback_query()
async def answer_gpt(message: Message):
    await message.answer("Больше возможностей помочь вы найдете в WebApp приложении по кнопке ниже.",
                         reply_markup=web_kb)
