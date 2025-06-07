import asyncio
from pathlib import Path

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, FSInputFile, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from states import TestStates

router = Router()

ANSWERS_PATH = Path("data/answers.txt")
TESTS_PATH = Path("data/tests")


@router.callback_query(TestStates.choosing_direction, F.data == "A4")
async def choose_direction(call: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="Test1", callback_data="A4:Test1")
    await call.message.answer("Testni tanlang:", reply_markup=builder.as_markup())
    await call.answer()
    await call.message.state.set_state(TestStates.choosing_test)


async def schedule_alerts(message: Message):
    alerts = [
        (30, "2:30 qoldi"),
        (60, "2 soat qoldi"),
        (90, "1:30 qoldi"),
        (120, "1 soat qoldi"),
        (150, "30 daqiqa qoldi"),
        (170, "10 daqiqa qoldi"),
    ]
    tasks = []
    for minutes, text in alerts:
        delay = minutes * 60
        tasks.append(asyncio.create_task(asyncio.sleep(delay)))
        tasks[-1].add_done_callback(lambda _, m=message, t=text: asyncio.create_task(m.answer(t)))
    return tasks


@router.callback_query(TestStates.choosing_test)
async def send_test(call: CallbackQuery):
    direction, test_name = call.data.split(":")
    file_path = TESTS_PATH / f"{direction}_{test_name}.pdf"
    if not file_path.exists():
        await call.answer("Fayl topilmadi", show_alert=True)
        return
    await call.message.answer_document(FSInputFile(file_path))
    await call.message.answer("Javoblaringizni 3 soat ichida yuboring.")
    tasks = await schedule_alerts(call.message)
    await call.message.state.update_data(alert_tasks=tasks, selected=f"{direction}:{test_name}")
    await call.message.state.set_state(TestStates.waiting_answers)
    await call.answer()

