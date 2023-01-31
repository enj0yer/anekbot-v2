from aiogram import Router, types

from classes.controllers import process_user

ROUTER = Router()


async def welcome(message: types.Message):
    result = process_user(message, save_changes=True)
    if not result:
        return
    await message.answer(f"Приветствую, {(('@' + message.from_user.username) if message.from_user.username else 'Ghost')}"
                         f"\n\n/joke для получения анекдота\n/help для просмотра остальных возможностей возможностей")