from pathlib import Path
from typing import List, Dict

import pandas as pd


def load_faq_from_excel(
    file_path: str,
    question_column: str,
    answer_column: str,
) -> List[Dict[str, str]]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"FAQ file not found: {file_path}")

    df = pd.read_excel(path)

    required_columns = {question_column, answer_column}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Missing required FAQ columns: {missing}")

    df = df.dropna(subset=[question_column, answer_column]).copy()

    records = []
    for idx, row in df.iterrows():
        question = str(row[question_column]).strip()
        answer = str(row[answer_column]).strip()

        if not question or not answer:
            continue

        records.append(
            {
                "id": idx + 1,
                "question": question,
                "answer": answer,
            }
        )

    return records
