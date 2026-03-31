import re
from dataclasses import dataclass

from app.services.files import load_stopwords_from_files


@dataclass
class StopWordsResult:
    passed: bool
    reason: str | None = None


class StopWordsAgent:
    def __init__(self, stopword_files: list[str]):
        self.stopwords = load_stopwords_from_files(stopword_files)
        print("[AGENT] loaded stopwords sample:", list(self.stopwords)[:20])

    @staticmethod
    def normalize_text(text: str) -> list[str]:
        text = text.lower().replace("ё", "е")
        return re.findall(r"[а-яa-z0-9]+", text, flags=re.IGNORECASE)

    @staticmethod
    def normalize_word(word: str) -> str:
        return word.lower().replace("ё", "е").strip()

    def check(self, text: str) -> StopWordsResult:
        tokens = self.normalize_text(text)
        print("[CHECK] tokens:", tokens)

        normalized_stopwords = {self.normalize_word(w) for w in self.stopwords}

        for token in tokens:
            token_norm = self.normalize_word(token)

            # точное совпадение
            if token_norm in normalized_stopwords:
                print("[MATCH] exact:", token_norm)
                return StopWordsResult(
                    passed=False,
                    reason=f"Forbidden token detected: {token_norm}",
                )

            # частичное совпадение
            for bad_word in normalized_stopwords:
                if bad_word in token_norm or token_norm in bad_word:
                    print("[MATCH] partial:", token_norm, "->", bad_word)
                    return StopWordsResult(
                        passed=False,
                        reason=f"Forbidden token detected: {token_norm}",
                    )

        print("[CHECK] no match")
        return StopWordsResult(passed=True)
