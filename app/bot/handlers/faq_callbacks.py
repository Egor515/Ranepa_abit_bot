from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.agents.faq_retrieval_agent import FAQRetrievalAgent

router = Router()

faq_agent = FAQRetrievalAgent()


@router.callback_query(F.data.startswith("faq:"))
async def faq_callback_handler(callback: CallbackQuery) -> None:
    data = callback.data or ""

    if data == "faq:none":
        await callback.message.answer(
            "Хорошо, подходящий FAQ не найден. Следующим этапом подключим SQL/Grok ветку."
        )
        await callback.answer()
        return

    faq_id = int(data.replace("faq:", "", 1))
    faq_item = faq_agent.get_by_id(faq_id)

    if faq_item is None:
        await callback.message.answer("Не удалось найти выбранный FAQ.")
        await callback.answer()
        return

    await callback.message.answer(faq_item.answer)
    await callback.answer()
