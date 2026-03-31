from pymilvus import MilvusClient


class MilvusFAQStore:
    def __init__(self, uri: str = "./milvus_faq.db", collection_name: str = "faq_collection"):
        self.client = MilvusClient(uri=uri)
        self.collection_name = collection_name

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
