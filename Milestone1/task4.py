import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

# ----------- 1. Load .env -----------
load_dotenv()

# get your key from .env
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# give your index any name
INDEX_NAME = "demo-index"

if not PINECONE_API_KEY:
    raise ValueError("❌ PINECONE_API_KEY missing in .env file")

# ----------- 2. Connect to Pinecone -----------
pc = Pinecone(api_key=PINECONE_API_KEY)
print("Connected to Pinecone!")

# ----------- 3. Create Index -----------
existing = pc.list_indexes().names()

if INDEX_NAME not in existing:
    pc.create_index(
        name=INDEX_NAME,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )
    print(f"Index '{INDEX_NAME}' created!")
else:
    print(f"Index '{INDEX_NAME}' already exists!")

# connect to index
index = pc.Index(INDEX_NAME)

# ----------- 4. CRUD -----------

# CREATE (upsert)
print("\n--- CREATE ---")
index.upsert(
    vectors=[
        {
            "id": "vec1",
            "values": [0.11] * 384,
            "metadata": {
                "text": "This is my first vector stored in Pinecone."
            }
        }
    ]
)

# READ (fetch)
print("\n--- READ ---")
res = index.fetch(ids=["vec1"])
print("Metadata:", res.vectors["vec1"].metadata["text"])

# UPDATE
print("\n--- UPDATE ---")
index.update(
    id="vec1",
    set_metadata={
        "text": "The vector metadata has been updated successfully."
    }
)

res2 = index.fetch(ids=["vec1"])
print("After update:", res2.vectors["vec1"].metadata["text"])


# # DELETE
# print("\n--- DELETE ---")
# index.delete(ids=["vec1"])
# res3 = index.fetch(ids=["vec1"])
# print("After delete:", res3.vectors)    # should be {}


# print("\nFinished CRUD operations!")
