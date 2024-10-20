from os.path import split
from aiogram import Dispatcher, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.orm import Session
from database.database import session_local, Base, engine
from database.models import User

bot = Bot(token='{{sensitive data}}')
dp = Dispatcher()
Base.metadata.create_all(bind=engine)

link = 'https://t.me/{{sensitive data}}'
print(link)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


async def create_user(name: str, telegram_id: int, db: Session) -> User | None:
    db_contains = db.query(User).filter(User.name == name).first()
    if db_contains is None:
        db_user = User(name=name, telegram_id=telegram_id)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    print("user already exists")


@dp.message(CommandStart())
async def send_welcome(message: Message):
    await message.answer(text=str(message.from_user.id))
    if len(split(message.text)) > 1:
        user_info = {
            'telegram_id': message.from_user.id,
            'name': message.from_user.username,
        }

        # Получаем сессию базы данных вручную
        db = session_local()
        try:
            await create_user(
                telegram_id=user_info['telegram_id'],
                name=user_info['name'],
                db=db  # Передаем сессию базы данных
            )
        finally:
            db.close()  # Закрываем сессию после использования

        print(user_info)
    else:
        await message.answer(id=message.chat.id, text=f'hello {message.from_user.username}')


# async def notification(list_of_users: list[User], user_id: int):
#     if list_of_users[0].telegram_id == user_id:
#         await bot.send_message(chat_id=user_id, text='Внимание сейчас ваша очередь!')

if __name__ == '__main__':
    dp.run_polling(bot)
