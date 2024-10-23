from aiogram import Dispatcher, types
from aiogram.filters import Command

from app.llm_client import generate_response
from app.message_store import save_message, get_user_messages, get_frequent_questions, get_all_users


# Обработчик команды /start
async def start_command(message: types.Message):
    await message.answer("Привет! Я готов ответить на твои вопросы.")


# Обработчик запросов к базе данных
async def handle_database_query(message: types.Message):
    user_id = message.from_user.id
    text = message.text.lower()

    # Запрос на получение информации о пользователях, которые общались с ботом
    if "кто с тобой общался" in text or "кто общался" in text:
        # Получение всех пользователей из базы данных
        response = get_all_users()
        await message.answer(f"С ботом общались следующие пользователи: {response}")

    # Запрос на получение последних сообщений пользователя
    elif "последний раз" in text:
        response = get_user_messages(user_id)
        await message.answer(f"Ваши последние сообщения: {response}")

    # Запрос на получение часто задаваемых вопросов
    elif "часто задают" in text or "вопросы" in text:
        response = get_frequent_questions()
        await message.answer(f"Часто задаваемые вопросы: {response}")

    # Иначе обрабатываем через LLM
    else:
        response = await generate_response(text)
        await message.answer(response)


def register_handlers(dp: Dispatcher):
    dp.message.register(start_command, Command(commands=["start"]))
    dp.message.register(handle_database_query)
