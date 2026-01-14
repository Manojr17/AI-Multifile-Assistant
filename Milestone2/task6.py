import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredHTMLLoader,
    TextLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

# Correct Data Folder
DATA_FOLDER = "../Data/"
INDEX_NAME = "milestone-index"

# Load API Key
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")


# --------- 1. Load documents ---------
def load_documents():
    docs = []
    for file in os.listdir(DATA_FOLDER):
        path = os.path.join(DATA_FOLDER, file)
        try:
            if file.lower().endswith(".pdf"):
                docs.extend(PyPDFLoader(path).load())

            elif file.lower().endswith(".docx"):
                docs.extend(Docx2txtLoader(path).load())

            elif file.lower().endswith(".html"):
                docs.extend(UnstructuredHTMLLoader(path).load())

            elif file.lower().endswith(".txt"):
                docs.extend(TextLoader(path, encoding="utf-8").load())

            print(f"Loaded: {file}")

        except Exception as e:
            print(f"[ERROR] Could not load {file}: {e}")

    return docs


# --------- 2. Split documents ---------
def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200
    )
    return splitter.split_documents(docs)


# --------- 3. Init Pinecone Index ---------
def init_pinecone():
    pc = Pinecone(api_key=PINECONE_API_KEY)

    if INDEX_NAME not in pc.list_indexes().names():
        pc.create_index(
            name=INDEX_NAME,
            dimension=384,  # MiniLM model output
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
        print("Created new Pinecone index.")
    else:
        print("Using existing Pinecone index.")

    return pc.Index(INDEX_NAME)


# --------- 4. Upload chunks manually (NO LANGCHAIN EMBEDDINGS) ---------
def upload_chunks(chunks):

    # Load MiniLM model directly
    model = SentenceTransformer("all-MiniLM-L6-v2")

    index = init_pinecone()

    vectors = []
    ids = []
    metadata_list = []

    for i, chunk in enumerate(chunks):
        vector = model.encode(chunk.page_content).tolist()

        ids.append(f"doc-{i}")
        vectors.append(vector)
        metadata_list.append({"text": chunk.page_content})

    try:
        index.upsert(vectors=zip(ids, vectors, metadata_list))
        print("Uploaded chunks to Pinecone.")

    except Exception as e:
        print("Error uploading to Pinecone:", e)


# --------- Main ---------
def run_task6():
    docs = load_documents()
    print("Total documents loaded:", len(docs))

    chunks = split_documents(docs)
    print("Total chunks:", len(chunks))

    upload_chunks(chunks)


run_task6()
