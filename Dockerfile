FROM python:3.10.9-slim

WORKDIR /

COPY ./requirements.txt /semantic_search/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /semantic_search/requirements.txt

COPY ./app ./semantic_search/app
COPY ./config.py /semantic_search/config.py

WORKDIR /semantic_search

ENV BASE_DIR=/semantic_search
ENV MEDIA=media
ENV PINECONE_API_KEY=pinecone_api_key

EXPOSE 8000

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]