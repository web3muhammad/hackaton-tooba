from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from src.bot.routers import main_router

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

dp.include_router(main_router)
