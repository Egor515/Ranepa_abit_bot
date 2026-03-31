from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def build_faq_keyboard(candidates: list[dict]) -> InlineKeyboardMarkup:
    buttons = []

    for candidate in candidates:
        buttons.append([
            InlineKeyboardButton(
                text=candidate["question"][:80],
                callback_data=f"faq:{candidate['id']}"
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            text="Нет подходящего ответа",
            callback_data="faq:none"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
