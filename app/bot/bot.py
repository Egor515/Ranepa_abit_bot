from aiogram import Bot, Dispatcher

from app.bot.handlers.start import router as start_router
from app.bot.handlers.messages import router as message_router
from app.bot.handlers.faq_callbacks import router as faq_callback_router
from app.core.config import settings


def create_bot() -> Bot:
    return Bot(token=settings.BOT_TOKEN)


def create_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    dp.include_router(start_router)
    dp.include_router(message_router)
    dp.include_router(faq_callback_router)
    return dp
