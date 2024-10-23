from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from app.config import TELEGRAM_BOT_TOKEN
from app.handlers import register_handlers

async def start_bot():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())  # Инициализация диспетчера с памятью для FSM

    register_handlers(dp)

    # Запуск бота
    await dp.start_polling(bot)
