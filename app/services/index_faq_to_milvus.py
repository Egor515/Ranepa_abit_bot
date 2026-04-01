from app.core.config import settings
from app.services.faq_loader import load_faq_from_excel
from app.services.embedding_service import EmbeddingService
from app.services.milvus_service import MilvusFAQStore


def main():
    faq_items = load_faq_from_excel(
        file_path=settings.FAQ_SOURCE_PATH,
        question_column=settings.FAQ_QUESTION_COLUMN,
        answer_column=settings.FAQ_ANSWER_COLUMN,
    )

    embedder = EmbeddingService()
    store = MilvusFAQStore()

    questions = [item["question"] for item in faq_items]
    vectors = embedder.embed_texts(questions)

    dim = len(vectors[0])
    store.recreate_collection(dim=dim)

    rows = []
    for item, vector in zip(faq_items, vectors):
        rows.append(
            {
                "id": item["id"],
                "vector": vector,
                "question": item["question"],
                "answer": item["answer"],
            }
        )

    store.insert(rows)
    print(f"Indexed {len(rows)} FAQ items into Milvus.")


if __name__ == "__main__":
    main()
