from pymilvus import MilvusClient

from app.core.config import settings


class MilvusFAQStore:
    def __init__(self, uri: str | None = None, collection_name: str | None = None):
        self.client = MilvusClient(uri=uri or settings.MILVUS_URI)
        self.collection_name = collection_name or settings.MILVUS_COLLECTION_NAME

    def recreate_collection(self, dim: int) -> None:
        existing = self.client.list_collections()
        if self.collection_name in existing:
            self.client.drop_collection(self.collection_name)

        self.client.create_collection(
            collection_name=self.collection_name,
            dimension=dim,
            metric_type="COSINE",
            auto_id=False,
        )

    def insert(self, rows: list[dict]) -> None:
        self.client.insert(
            collection_name=self.collection_name,
            data=rows,
        )

    def search(self, query_vector: list[float], limit: int = 5):
        return self.client.search(
            collection_name=self.collection_name,
            data=[query_vector],
            limit=limit,
            output_fields=["question", "answer"],
        )
