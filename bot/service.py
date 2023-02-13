from aiogram import types
from aiogram.types import ReplyKeyboardMarkup

from classes.base import Ban
from classes.controllers import UsersController
from utils.asserts import Asserts


async def send_ban_info(message: types.Message, ban: Ban):
    await message.answer(f'Вы были забанены {("модератором @" + str(UsersController().get_by_id(ban.from_user).username)) if ban.from_user else ""} {("по причине " + "`" + ban.cause + "`") if ban.cause else ""}')


class Answers:
    __UNKNOWN_CASE_ANSWER = "Не знаю, как на это ответить, попробуйте эти команды:\n\n/joke - получить анекдот\n/joke_from_category - получить анекдот из определенной категории\n/"

    @classmethod
    def unknown(cls):
        return cls.__UNKNOWN_CASE_ANSWER

    @staticmethod
    def welcome(message: types.Message):
        return f"Приветствую, {(('@' + message.from_user.username) if message.from_user.username else 'Ghost')}" \
               f"\n\n/joke для получения анекдота\n/help для просмотра остальных возможностей возможностей"


def make_keyboard(items: list[str], rows: int, cols: int):
    if rows or cols <= 0:
        raise AttributeError("Value of cols (rows) parameter should be non-negative")

    remaining_amount = len(items) / (rows + cols)

    items_matrix = None

    # if remaining_amount == 0:
    #     items_matrix =

