from pymilvus import (
    MilvusClient,
    DataType,
)


class MilvusStore:

    def __init__(
        self,
        uri: str = "http://localhost:19530",
    ):
        self.client = MilvusClient(uri=uri)

        self.collection_name = "process_knowledge"

    def create_collection(
        self,
        dimension: int,
    ):

        if self.client.has_collection(
            collection_name=self.collection_name
        ):
            return

        schema = self.client.create_schema(
            auto_id=True,
            enable_dynamic_field=True,
        )

        schema.add_field(
            field_name="id",
            datatype=DataType.INT64,
            is_primary=True,
        )

        schema.add_field(
            field_name="vector",
            datatype=DataType.FLOAT_VECTOR,
            dim=dimension,
        )

        index_params = self.client.prepare_index_params()

        index_params.add_index(
            field_name="vector",
            index_type="AUTOINDEX",
            metric_type="COSINE",
        )

        self.client.create_collection(
            collection_name=self.collection_name,
            schema=schema,
            index_params=index_params,
        )

    def insert(
        self,
        data: list[dict],
    ):

        return self.client.insert(
            collection_name=self.collection_name,
            data=data,
        )

    def search(
        self,
        query_vector: list[float],
        top_k: int = 3,
    ) -> list[dict]:

        results = self.client.search(
            collection_name=self.collection_name,
            data=[query_vector],
            limit=top_k,
            output_fields=[
                "text",
                "source",
                "title",
                "section",
                "material",
                "process",
            ],
            search_params={
                "metric_type": "COSINE",
            },
        )

        return results[0]

    # 删除collection
    def drop_collection(self):

        if self.client.has_collection(
            collection_name=self.collection_name
        ):
            self.client.drop_collection(
                collection_name=self.collection_name
            )