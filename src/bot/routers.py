from aiogram import Router
from src.bot.handlers import router

main_router = Router()

main_router.include_router(router)
