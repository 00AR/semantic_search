from io import BytesIO
from uuid import uuid4
from fastapi import HTTPException, UploadFile
from sentence_transformers import SentenceTransformer, util
import torch
import os

from app.utils.data_cleaner import read_pdf
from app.pinecone import pinecone_index
from config import settings



# Loading the pre-trained sentence transformer model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')


def generate_embeddings(text):
    return model.encode(text, convert_to_tensor=True)


async def insert_new_document(title: str, file: UploadFile):
    content = await file.read()
    text = read_pdf(BytesIO(content))
    text = text.replace('\n', ' ')
    embedding = generate_embeddings(text)
    index = pinecone_index()
    uid = str(uuid4())
    filename = file.filename.replace(" ", "_")
    path = f"{uid}_{filename}"
    with open(os.path.join(settings.BASE_DIR, settings.MEDIA, path), 'wb') as f:
        f.write(content)
    index.upsert([(uid, embedding.tolist(), {"title": title, "path": path, "filename": file.filename})])


async def get_results(query_text):
    index = pinecone_index()
    query = generate_embeddings(query_text)
    results = index.query(vector=query.tolist(), top_k=5, include_metadata=True)
    if not results["matches"]:
        raise HTTPException(status_code=404, detail="No matching case studies found.")
    return [match["metadata"] for match in results["matches"]]