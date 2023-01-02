import logging
from aiogram import Bot, Dispatcher, executor, types
from classes.User import User
from controllers.BansController import BansController
from controllers.UsersController import UsersController
from controllers.JokesController import JokesController
from config.settings import TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
db = Dispatcher(bot)


@db.message_handler(commands=['start'])
async def welcome(message: types.Message):
    controller = UsersController()
    controller.save(User(tg_id=message.from_user.id,
                         username=message.from_user.username,
                         first_name=message.from_user.first_name,
                         last_name=message.from_user.last_name))

    await message.answer(f"Приветствую, {message.from_user.username}.\n/joke - очередной анекдот")


@db.message_handler(commands=['joke'])
async def get(message: types.Message):
    controller = JokesController()
    random_joke = controller.get_random_joke()
    await message.answer(random_joke.data)


@db.message_handler(commands=['admin'])
async def admin(message: types.Message):
    pass


if __name__ == "__main__":
    executor.start_polling(db, skip_updates=True)


@db.message_handler()
async def other(message: types.Message):
    await message.answer("Не знаю, как на это ответить, попробуйте эти команды:\n/start\n/joke")