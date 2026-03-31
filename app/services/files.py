from pathlib import Path


def load_stopwords_from_files(file_paths: list[str]) -> set[str]:
    stopwords = set()

    for file_path in file_paths:
        path = Path(file_path)

        print(f"[LOAD] trying file: {path.resolve()}")

        if not path.exists():
            print(f"[LOAD] file not found: {file_path}")
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

    print(f"[LOAD] total stopwords: {len(stopwords)}")
    return stopwords
