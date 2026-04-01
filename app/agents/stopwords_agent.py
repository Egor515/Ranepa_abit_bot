import re
from dataclasses import dataclass

from app.core.logging import logger
from app.services.files import load_stopwords_from_files


@dataclass
class StopWordsResult:
    passed: bool
    reason: str | None = None


class StopWordsAgent:
    def __init__(self, stopword_files: list[str]):
        self.stopwords = {
            self.normalize_word(word)
            for word in load_stopwords_from_files(stopword_files)
            if self.normalize_word(word)
        }
        logger.debug("StopWordsAgent loaded {} normalized stopwords", len(self.stopwords))

    @staticmethod
    def normalize_word(word: str) -> str:
        return word.lower().replace("ё", "е").strip()

    @staticmethod
    def normalize_text(text: str) -> list[str]:
        text = text.lower().replace("ё", "е")
        return re.findall(r"[а-яa-z0-9]+", text, flags=re.IGNORECASE)

    def check(self, text: str) -> StopWordsResult:
        tokens = self.normalize_text(text)
        logger.debug("StopWordsAgent tokens: {}", tokens)

        for token in tokens:
            token_norm = self.normalize_word(token)

            if token_norm in self.stopwords:
                logger.info("StopWordsAgent blocked token: {}", token_norm)
                return StopWordsResult(
                    passed=False,
                    reason=f"Forbidden token detected: {token_norm}",
                )

        logger.debug("StopWordsAgent passed message")
        return StopWordsResult(passed=True)
