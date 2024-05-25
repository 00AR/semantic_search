from pinecone import Pinecone, ServerlessSpec
from config import settings

pc = Pinecone(api_key=settings.PINECONE_API_KEY)

index_name = "case-studies-index"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )

    )

def pinecone_index():
    return pc.Index(index_name)

