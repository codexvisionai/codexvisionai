import asyncio

from aiogram import Bot, Dispatcher

from config import load_config
from storage import get_storage
from handlers import start, payment, tests, answers


def register_handlers(dp: Dispatcher, config):
    dp.include_router(start.router)
    dp.include_router(payment.router)
    dp.include_router(tests.router)
    dp.include_router(answers.router)
    dp['config'] = config


async def main() -> None:
    config = load_config()
    bot = Bot(token=config.bot_token, parse_mode="HTML")
    dp = Dispatcher(storage=get_storage())
    register_handlers(dp, config)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

