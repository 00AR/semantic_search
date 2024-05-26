from uuid import uuid4
from fastapi import FastAPI, HTTPException, File, UploadFile, status
from fastapi.responses import FileResponse
import os


from app.metadata import extract_metadata
from app.utils.data_cleaner import read_pdf, text_to_pdf
from app.pinecone import pinecone_index
from app.semantic_search import generate_embeddings, get_results, insert_new_document
from config import settings

app = FastAPI()


# TODO: replace "search" with "docs"
@app.get("/search")
async def search(query: str):
    result = await get_results(query)
    return result


@app.post("/upload")
async def upload(
    title: str,
    file: UploadFile = File(...),
):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )
    await insert_new_document(title, file)
    return {"success": True, "message": "File uploaded!"}


@app.get("/media/{filename}")
async def get_file(file_path: str):
    pdf_file_path = f"./media/{file_path}"
    if not os.path.exists(pdf_file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="PDF file not found"
            )
    filename = pdf_file_path.split("/")[-1]
    return FileResponse(pdf_file_path, media_type='application/pdf', filename=filename)


@app.get("/generate_db")
async def generate_db():
    await insert_all_pdfs_to_pinecone()
    return {"message": "success"}


async def insert_all_pdfs_to_pinecone():
    # NOTE: Requires one PDF per case study stored in a directory named "media".
    # Use our functions in data_cleaner.py to create pdfs automatically from a
    # list of sample text files. The data in the text files will be cleaned
    # automatically to find case studies and will be saved in pdf format.

    media_dir = os.path.join(settings.BASE_DIR, settings.MEDIA)
    index = pinecone_index()
    index.delete(delete_all=True)
    if not os.path.exists(media_dir):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Directory does not exists"
            )
    for filename in os.listdir(os.path.join(settings.BASE_DIR, 'samples')):
        if filename.endswith('.pdf'):
            content = read_pdf(os.path.join(settings.BASE_DIR, 'samples', filename))
            title = ""
            pos = content.index('Industry:')
            title = content[:pos]
            title = title.replace('\n', '')
            
            content = content.replace('\n', ' ') # NOTE: this should be done before extracting title
            industry, use_case, geography = extract_metadata(content)
            embedding = generate_embeddings(content)
            uid = str(uuid4())
            fname = filename.split('_')[-1]
            path = f"{uid}_{fname}"
            text_to_pdf(content, os.path.join(media_dir, path))
            index.upsert([(uid, embedding.tolist(), {"title": title, "filename": path, "industry": industry, "geography": geography, "use_case": use_case})])
            