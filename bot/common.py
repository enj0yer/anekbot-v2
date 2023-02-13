from aiogram import Router, types
from aiogram.filters import Command

from classes.controllers import process_user, JokesController
from bot.service import Answers

router = Router()


@router.message(Command(commands=['start']))
async def welcome(message: types.Message):
    result = process_user(message)
    if not result:
        return
    await message.answer(Answers.welcome(message))


@router.message(Command(commands=['joke']))
async def get(message: types.Message):
    result = process_user(message)
    if not result:
        return
    controller = JokesController()
    random_joke = controller.get_random_joke()
    await message.answer(random_joke.data)


@router.message()
async def unknown(message: types.Message):
    result = process_user(message, save_changes=True)
    if not result:
        return
    await message.answer(Answers.unknown())
