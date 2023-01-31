from aiogram import types

from classes.base import Ban
from classes.controllers import UsersController


async def send_ban_info(message: types.Message, ban: Ban):
    await message.answer(f'Вы были забанены {("модератором @" + str(UsersController().get_by_id(ban.from_user).username)) if ban.from_user else ""} {("по причине " + "`" + ban.cause + "`") if ban.cause else ""}')
