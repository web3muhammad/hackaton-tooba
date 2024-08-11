from aiogram import Router
from src.app.bot.handlers import router

main_router = Router()

main_router.include_router(router)
