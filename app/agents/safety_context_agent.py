from dataclasses import dataclass
import json
import re

from app.prompts.safety import SAFETY_SYSTEM_PROMPT
from app.services.llm_client import GeminiLLMClient


@dataclass
class SafetyContextResult:
    decision: str
    reason: str
    reply: str


class SafetyContextAgent:
    MIN_LEN = 3

    def __init__(self):
        self.llm = GeminiLLMClient()

    def _cheap_checks(self, text: str) -> SafetyContextResult | None:
        raw_text = (text or "").strip()
        lowered = raw_text.lower()

        if not raw_text:
            return SafetyContextResult(
                decision="reject",
                reason="empty",
                reply="Я не понял запрос. Попробуйте сформулировать его яснее.",
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
                reply="Похоже, запрос состоит только из символов. Напишите вопрос текстом.",
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

        garbage_patterns = {"asdf", "qwer", "zxcv", "йцу", "фыва", "testtest"}
        if any(pattern in lowered for pattern in garbage_patterns):
            return SafetyContextResult(
                decision="reject",
                reason="garbage_pattern",
                reply="Похоже, запрос составлен некорректно. Попробуйте задать осмысленный вопрос.",
            )

        toxic_patterns = {
            "тупой", "идиот", "дурак", "дебил", "пошел", "ненавижу",
            "stupid", "idiot", "dumb", "hate"
        }
        if any(pattern in lowered for pattern in toxic_patterns):
            return SafetyContextResult(
                decision="reject",
                reason="toxic_language",
                reply="Пожалуйста, формулируйте запрос без оскорблений.",
            )

        return None

    def _parse_llm_json(self, raw: str) -> SafetyContextResult:
        try:
            parsed = json.loads(raw)
        except Exception:
            return SafetyContextResult(
                decision="clarify",
                reason="invalid_llm_output",
                reply="Пожалуйста, уточните ваш вопрос.",
            )

        decision = parsed.get("decision", "clarify")
        reason = parsed.get("reason", "unknown")
        reply = parsed.get("reply", "Пожалуйста, уточните ваш вопрос.")

        if decision not in {"allow", "reject", "clarify"}:
            return SafetyContextResult(
                decision="clarify",
                reason="invalid_decision",
                reply="Пожалуйста, уточните ваш вопрос.",
            )

        if not isinstance(reason, str):
            reason = str(reason)

        if not isinstance(reply, str) or not reply.strip():
            reply = "Пожалуйста, уточните ваш вопрос."

        return SafetyContextResult(
            decision=decision,
            reason=reason,
            reply=reply.strip(),
        )

    def check(self, text: str) -> SafetyContextResult:
        cheap_result = self._cheap_checks(text)
        if cheap_result is not None:
            return cheap_result

        user_prompt = f"Пользовательское сообщение:\n{text}"

        try:
            raw = self.llm.generate(
                system_prompt=SAFETY_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                response_mime_type="application/json",
            )
            return self._parse_llm_json(raw)

        except Exception as e:
            lowered = (text or "").lower()

            toxic_markers = {
                "тупой", "идиот", "дурак", "дебил", "ненавижу",
                "пошел", "stupid", "idiot", "hate"
            }

            if any(marker in lowered for marker in toxic_markers):
                return SafetyContextResult(
                    decision="reject",
                    reason="fallback_toxicity_detected",
                    reply="Пожалуйста, формулируйте запрос без оскорблений.",
                )

            return SafetyContextResult(
                decision="clarify",
                reason=f"llm_error: {type(e).__name__}",
                reply="Пожалуйста, уточните ваш вопрос.",
            )
