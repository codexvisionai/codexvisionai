from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import Config
from states import TestStates

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, config: Config):
    await message.answer("Assalomu alaykum! Testga kirish uchun to'lovni amalga oshiring.")

    prices = [LabeledPrice(label="Test to'lovi", amount=1000)]
    await message.answer_invoice(
        title="Test to'lovi",
        description="Test uchun to'lov",
        provider_token=config.provider_token,
        currency="UZS",
        prices=prices,
        payload="test-payment",
    )
    await message.state.set_state(TestStates.waiting_for_payment)
