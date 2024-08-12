from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from src.config import settings

inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Помочь", callback_data='help')]]
)

web_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Открыть", web_app=WebAppInfo(url=settings.WEBAPP))]]
)