# Semantic Search Engine API
This project allows a user to make semantic search on the database of case studies. 
User can upload more case studies in the pdf format. 
The case studies are stored as index of vectors in a vector database hosted on cloud,
namely, Pinecone.

## Setup
To setup the project on your local machine, do the following
- Clone the repo
    ```bash
    git clone repo_link
    cd semantic_search
    ```
- Make a python virtual environment
    ```bash
    python -m venv .env
    ```
- Activate the virtual environment
    ```bash
    source .env/bin/activate
    ```
- Install Requirements
    ```bash
    pip install -r requirements.txt
    ```
- Setup Environment Variables
    - Create a new file named `.config.env` and add the following:
        ```bash
        BASE_DIR=/path/to/the/repo/semantic_search
        MEDIA=media
        PINECONE_API_KEY=your_pinecone_api_key
        ```
- Run app using
    ```bash
    uvicorn app.main:app
    ```
### Setup using docker file Docker(**Note**: use sudo incase of permission denied error):
- build the image using 
    ```bash
    docker build -t semantic-search-app .
    ```
- Run the docker image
    ```bash
    docker run -p 8000:8000 -e pinecone_api_key=your_api_key semantic-search-app
    ```
## APIs
![apis](images/apis.png)
## Working
### `/search` endpoint
The project is built using fastapi. It uses Pinecone Vector database for storing embeddings.
When the user enters a search term on `/search` endpoint, the query is converted into an embedding.
The embedding is then matched with the embeddings of the case studies using cosine similarity that are stored in pinecone.
The best matches are returned as response. The response includes a `title` and `path`. 
### `/upload` endpoint
User can upload a case study file in pdf format through `/upload` endpoint.
### `/media/{filename}` endpoint
Additionally user can download the case of interest from `/media/{filename}` endpoint. The `path` from the search results of `/search` must supplied as filename to this endpoint.
### `/generate_db` endpoint
This will regenerate the embeddings and store them on an empty pinecone database index. It uses case studies stored in `samples` folder. `samples` store one pdf per one case study.