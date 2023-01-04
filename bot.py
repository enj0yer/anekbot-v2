import logging
from aiogram import Bot, Dispatcher, executor, types
from classes.base import User
from classes.controllers import BansController, UsersController, JokesController, LikesController
from config.settings import TOKEN
from classes.enums import Role

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
db = Dispatcher(bot)


@db.message_handler(commands=['start'])
async def welcome(message: types.Message):
    controller = UsersController()
    user = controller.get_by_tg_id(message.from_user.id)
    if not user:
        controller.save(User(tg_id=message.from_user.id,
                             username=message.from_user.username,
                             first_name=message.from_user.first_name,
                             last_name=message.from_user.last_name,
                             role=Role.USER))
    else:
        controller.save(User(user_id=user.id, username=message.from_user.username, first_name=message.from_user.first_name, last_name=message.from_user.last_name, role=user.role))

    await message.answer(f"Приветствую, {message.from_user.username}.\n/joke - очередной анекдот")


@db.message_handler(commands=['joke'])
async def get(message: types.Message):
    ban = UsersController.is_banned(User(tg_id=message.from_user.id))
    if ban:
        await message.answer(f'Вы были забанены {("модератором " + str(UsersController().get_by_id(ban.from_user).username)) if ban.from_user else ""} {("по причине " + "`" + ban.cause + "`") if ban.cause else ""}')
        return
    controller = JokesController()
    random_joke = controller.get_random_joke()
    await message.answer(random_joke.data)
    return


@db.message_handler(commands=['admin'])
async def admin(message: types.Message):
    pass


if __name__ == "__main__":
    executor.start_polling(db, skip_updates=True)


@db.message_handler()
async def other(message: types.Message):
    await message.answer("Не знаю, как на это ответить, попробуйте эти команды:\n/start\n/joke")
