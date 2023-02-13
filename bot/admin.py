from aiogram import Router, types
from aiogram.filters import Command

from classes.controllers import process_user, UsersController
from classes.enums import Role

router = Router()


@router.message(Command(commands=['admin']))
async def admin(message: types.Message):
    result = process_user(message)
    if not result:
        return

    role = UsersController().get_role(message.from_user.id)

    if role not in Role.with_admin_access():
        return


