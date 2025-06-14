import asyncio
from aiogram import Bot, Dispatcher
from config import TELEGRAM_TOKEN
from database import init_db
from handlers import commands, buttons, messages
from aiogram.client.default import DefaultBotProperties
from monitor import monitor_servers  # если в отдельном файле


async def main():
    init_db()
    bot = Bot(
        token=TELEGRAM_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )

    dp = Dispatcher()

    dp.include_router(commands.router)
    dp.include_router(buttons.router)
    dp.include_router(messages.router)
    asyncio.create_task(monitor_servers(bot))

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
