from aiogram import Router
from aiogram.types import Message

from app.bot.keyboards.faq_keyboard import build_faq_keyboard
from app.core.container import get_pipeline
from app.services.session_store import session_store

router = Router()


@router.message()
async def handle_user_message(message: Message) -> None:
    user_text = message.text or ""
    user_id = message.from_user.id
    pipeline = get_pipeline()
    state = pipeline.handle_question(user_id=user_id, text=user_text)
    session_store.set_state(user_id, state)

    if state.has_faq_candidates:
        keyboard = build_faq_keyboard(
            [{"id": candidate.id, "question": candidate.question} for candidate in state.faq_candidates]
        )
        await message.answer(
            "Я нашел похожие вопросы. Выберите подходящий вариант:",
            reply_markup=keyboard,
        )
        return

    await message.answer(state.final_answer or "Не удалось обработать запрос.")
