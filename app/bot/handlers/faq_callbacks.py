from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.core.container import get_pipeline
from app.services.session_store import session_store

router = Router()


@router.callback_query(F.data.startswith("faq:"))
async def faq_callback_handler(callback: CallbackQuery) -> None:
    data = callback.data or ""
    user_id = callback.from_user.id
    state = session_store.get_state(user_id)

    if state is None:
        await callback.message.answer(
            "Сессия с вариантами FAQ истекла. Пожалуйста, задайте вопрос заново."
        )
        await callback.answer()
        return

    pipeline = get_pipeline()
    faq_id = None if data == "faq:none" else int(data.replace("faq:", "", 1))
    updated_state = pipeline.handle_faq_selection(state=state, faq_id=faq_id)
    session_store.set_state(user_id, updated_state)

    await callback.message.answer(updated_state.final_answer or "Не удалось обработать выбор FAQ.")
    await callback.answer()
