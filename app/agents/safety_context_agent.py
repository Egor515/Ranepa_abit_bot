from dataclasses import dataclass
import re


@dataclass
class SafetyContextResult:
    decision: str   # allow / reject / clarify
    reason: str
    reply: str


class SafetyContextAgent:
    MIN_LEN = 3

    def check(self, text: str) -> SafetyContextResult:
        raw_text = (text or "").strip()
        lowered = raw_text.lower()

        if not raw_text:
            return SafetyContextResult(
                decision="reject",
                reason="empty",
                reply="Я не понял запрос. Попробуйте сформулировать его более ясно.",
            )

        if len(lowered) < self.MIN_LEN:
            return SafetyContextResult(
                decision="clarify",
                reason="too_short",
                reply="Запрос слишком короткий. Пожалуйста, опишите вопрос подробнее.",
            )

        if re.fullmatch(r"[^\wа-яА-Яa-zA-Z0-9]+", raw_text):
            return SafetyContextResult(
                decision="reject",
                reason="symbols_only",
                reply="Похоже, запрос состоит только из символов. Попробуйте сформулировать вопрос текстом.",
            )

        if re.fullmatch(r"(.)\1{4,}", lowered):
            return SafetyContextResult(
                decision="reject",
                reason="repeated_chars",
                reply="Похоже, запрос составлен некорректно. Попробуйте написать его обычным текстом.",
            )

        letters_only = re.sub(r"[^а-яa-z]", "", lowered, flags=re.IGNORECASE)
        if letters_only and len(set(letters_only)) <= 2 and len(letters_only) >= 6:
            return SafetyContextResult(
                decision="clarify",
                reason="low_information",
                reply="Я не совсем понял вопрос. Попробуйте переформулировать его более понятно.",
            )

        garbage_patterns = {
            "asdf", "qwer", "zxcv", "йцу", "фыва", "лолкек", "testtest"
        }
        if any(pattern in lowered for pattern in garbage_patterns):
            return SafetyContextResult(
                decision="reject",
                reason="garbage_pattern",
                reply="Похоже, запрос составлен некорректно. Попробуйте задать осмысленный вопрос.",
            )

        return SafetyContextResult(
            decision="allow",
            reason="ok",
            reply="OK",
        )
