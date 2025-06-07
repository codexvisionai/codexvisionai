from aiogram import F
from aiogram import Router
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import PreCheckoutQuery, Message

from states import TestStates

router = Router()


@router.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@router.message(TestStates.waiting_for_payment, F.successful_payment)
async def successful_payment(message: Message):
    await message.answer("To'lov muvaffaqiyatli amalga oshirildi. Yo'nalishni tanlang.")
    kb = [[{"text": "A4", "callback_data": "A4"}]]
    await message.answer("Yo'nalishni tanlang:", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))
    await message.state.set_state(TestStates.choosing_direction)
