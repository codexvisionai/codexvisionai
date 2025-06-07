from pathlib import Path

from aiogram import Router
from aiogram.types import Message
from aiogram import F

from states import TestStates

router = Router()

ANSWERS_PATH = Path("data/answers.txt")


def load_answers() -> dict:
    results = {}
    with ANSWERS_PATH.open() as f:
        for line in f:
            direction, test_name, answers = line.strip().split(":")
            results[f"{direction}:{test_name}"] = answers
    return results


@router.message(TestStates.waiting_answers, F.text)
async def receive_answers(message: Message):
    data = await message.state.get_data()
    selected = data.get("selected")
    tasks = data.get("alert_tasks", [])
    for t in tasks:
        t.cancel()
    answers_map = load_answers()
    correct_answers = answers_map.get(selected)
    if not correct_answers:
        await message.answer("Test javoblari topilmadi")
        return
    user_ans = message.text.strip().lower()
    results = []
    correct_count = 0
    for i, user_a in enumerate(user_ans):
        correct = correct_answers[i] if i < len(correct_answers) else None
        if user_a == correct:
            results.append(f"{i+1}) {user_a.upper()} \u2705")
            correct_count += 1
        else:
            results.append(f"{i+1}) Siz: {user_a.upper()} | To'g'ri: {correct.upper() if correct else '-'} \u274c")
    await message.answer("\n".join(results))
    await message.answer(f"Jami to'g'ri javoblar: {correct_count}")
    await message.state.clear()

