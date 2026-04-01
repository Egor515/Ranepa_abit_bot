from pathlib import Path

from app.core.logging import logger


def load_stopwords_from_files(file_paths: list[str]) -> set[str]:
    stopwords = set()

    for file_path in file_paths:
        path = Path(file_path)
        logger.debug("Loading stopwords from {}", path.resolve())

        if not path.exists():
            logger.warning("Stopwords file not found: {}", file_path)
            continue

        with path.open("r", encoding="utf-8-sig") as f:
            for line in f:
                word = line.strip().lower()

                if not word:
                    continue

                # убираем возможные кавычки и лишние пробелы
                word = word.strip("\"'`.,;:!?()[]{} ")

                if word:
                    stopwords.add(word)

    logger.info("Loaded {} stopwords", len(stopwords))
    return stopwords
