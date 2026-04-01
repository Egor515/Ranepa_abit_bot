from dataclasses import dataclass
from typing import List

from app.services.embedding_service import EmbeddingService
from app.services.milvus_service import MilvusFAQStore


@dataclass
class FAQCandidate:
    id: int
    question: str
    answer: str
    score: float


class FAQRetrievalAgent:
    def __init__(self):
        self.embedder = EmbeddingService()
        self.store = MilvusFAQStore()

    def search(self, query: str, top_k: int = 5, threshold: float = 0.95) -> List[FAQCandidate]:
        query_vector = self.embedder.embed_text(query)
        results = self.store.search(query_vector=query_vector, limit=top_k)

        candidates = []
        for hit in results[0]:
            score = float(hit["distance"])
            entity = hit["entity"]

            if score < threshold:
                continue

            candidates.append(
                FAQCandidate(
                    id=int(hit["id"]),
                    question=entity["question"],
                    answer=entity["answer"],
                    score=score,
                )
            )

        return candidates

    def get_by_id(self, faq_id: int) -> FAQCandidate | None:
        records = self.store.client.get(
            collection_name=self.store.collection_name,
            ids=[faq_id],
            output_fields=["question", "answer"],
        )

        if not records:
            return None

        item = records[0]
        return FAQCandidate(
            id=int(item["id"]),
            question=item["question"],
            answer=item["answer"],
            score=1.0,
        )
