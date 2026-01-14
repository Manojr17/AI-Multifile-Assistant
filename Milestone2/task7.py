import os
from dotenv import load_dotenv
load_dotenv()

from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

INDEX_NAME = "milestone-index"

# Load API key
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Load embedding model (same as Task 6)
model = SentenceTransformer("all-MiniLM-L6-v2")

def run_task7(query):

    # 1. Connect to Pinecone
    pc = Pinecone(api_key=PINECONE_API_KEY)

    # 2. Load existing index
    index = pc.Index(INDEX_NAME)

    # 3. Convert query to embedding
    query_vec = model.encode(query).tolist()

    # 4. Perform similarity search
    results = index.query(
        vector=query_vec,
        top_k=4,
        include_metadata=True
    )

    # 5. Print results
    print("\nTop 4 Matches:\n")
    for i, match in enumerate(results["matches"], start=1):
        text = match["metadata"]["text"][:300]  # Print first 300 chars
        score = match["score"]
        print(f"Result {i} (Score: {score:.4f}):\n{text}\n")


# ------- Test -------
if __name__ == "__main__":
    run_task7("What does the document say about Indian constitution?")
