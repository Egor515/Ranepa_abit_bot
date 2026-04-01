import asyncio

from app.bot.bot import create_bot, create_dispatcher
from app.core.logging import configure_logging


async def main():
    configure_logging()
    bot = create_bot()
    dp = create_dispatcher()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
    asyncio.run(main())
