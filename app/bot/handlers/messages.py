from aiogram import Router
from aiogram.types import Message

from app.agents.stopwords_agent import StopWordsAgent
from app.agents.safety_context_agent import SafetyContextAgent
from app.agents.faq_retrieval_agent import FAQRetrievalAgent
from app.bot.keyboards.faq_keyboard import build_faq_keyboard

router = Router()

stopwords_agent = StopWordsAgent([
    "data/ru_abusive_words.txt",
    "data/ru_curse_words.txt",
])

safety_context_agent = SafetyContextAgent()
faq_agent = FAQRetrievalAgent()


@router.message()
async def handle_user_message(message: Message) -> None:
    user_text = message.text or ""

    stopwords_result = stopwords_agent.check(user_text)
    if not stopwords_result.passed:
        await message.answer(
            "Я не буду отвечать на сообщения с ненормативной лексикой."
        )
        return

    safety_result = safety_context_agent.check(user_text)
    if safety_result.decision in {"reject", "clarify"}:
        await message.answer(safety_result.reply)
        return

    candidates = faq_agent.search(user_text, top_k=5, threshold=0.65)

    if not candidates:
        await message.answer(
            "Я не нашел FAQ с достаточной близостью. Нажмите позже 'Нет подходящего ответа' — эту ветку мы подключим следующей."
        )
        return

    keyboard = build_faq_keyboard([
        {"id": c.id, "question": c.question}
        for c in candidates
    ])

    await message.answer(
        "Я нашел похожие вопросы. Выберите подходящий вариант:",
        reply_markup=keyboard,
    )
