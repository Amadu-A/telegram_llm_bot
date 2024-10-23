from app.database import SessionLocal, User, Message
from sqlalchemy.sql import func


def get_all_users():
    """Возвращает список всех пользователей, которые общались с ботом."""
    with SessionLocal() as session:
        users = session.query(User).all()
        if not users:
            return "С ботом пока никто не общался."

        # Формирование списка пользователей
        user_names = [
            f"{user.first_name} {user.last_name}" if user.first_name or user.last_name else f"User ID {user.id}" for
            user in users]
        return ", ".join(user_names)


def save_message(user_id: int, content: str):
    """Сохраняет сообщение пользователя в базе данных."""
    # Создаем новую сессию
    with SessionLocal() as session:
        # Проверяем, существует ли пользователь
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            # Если пользователь не найден, создаем нового
            user = User(id=user_id)
            session.add(user)

        # Сохраняем сообщение
        message = Message(user_id=user_id, content=content)
        session.add(message)
        session.commit()

def get_user_messages(user_id: int):
    """Извлекает все сообщения пользователя из базы данных."""
    with SessionLocal() as session:
        messages = session.query(Message).filter(Message.user_id == user_id).all()
        if not messages:
            return "Нет сообщений от этого пользователя."

        # Формируем список сообщений
        message_texts = [msg.content for msg in messages]
        return "\n".join(message_texts)

def get_frequent_questions():
    """Возвращает список наиболее часто задаваемых вопросов."""
    with SessionLocal() as session:
        # Группируем сообщения по содержимому и считаем количество повторений
        question_counts = session.query(Message.content, func.count(Message.content).label('count')) \
                                 .group_by(Message.content) \
                                 .order_by(func.count(Message.content).desc()) \
                                 .all()
        if not question_counts:
            return "Нет часто задаваемых вопросов."

        # Формируем список часто задаваемых вопросов
        frequent_questions = [f"{content} — {count} раз(а)" for content, count in question_counts]
        return "\n".join(frequent_questions)
