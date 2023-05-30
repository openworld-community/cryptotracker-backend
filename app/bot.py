import logging

# Aiogram imports
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.types import (
    ParseMode,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils import executor

import requests

logging.basicConfig(level=logging.INFO)

token = "6098476096:AAGHeQTGSEyyzp_SBOnI23VtT2JOUkeAzL0"

bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start", "help"])
async def welcome_handler(message: types.Message):
    uid = message.from_user.id  # Not neccessary, just to make code shorter

    # If user doesn't exist in database, insert it
    if not db.check_user(uid):
        db.add_user(uid)

    # Keyboard with two main buttons: Deposit and Balance
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(KeyboardButton("Deposit"))
    keyboard.row(KeyboardButton("Balance"))

    # Send welcome text and include the keyboard
    await message.answer(
        "Hi!\nI am example bot " "Use keyboard to test my functionality.",
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN,
    )
