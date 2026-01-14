import os, json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import (
    PDFPlumberLoader,
    Docx2txtLoader,
    TextLoader,
    UnstructuredHTMLLoader
)

# ==== EMBEDDING MODEL ====
embedder = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ==== FOLDER PATH (instead of list of files) ====
data_folder = r"C:\Users\dell\OneDrive\Desktop\Ai-Based Smart File Assistant For Contextual Querying And Efficient Information Extraction From Multiple Documents\Data"


# Process only these file types
allowed_exts = {".pdf", ".docx", ".txt", ".html"}

# ==== SPLITTER ====
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

# LOOP THROUGH ALL FILES IN FOLDER
for file_name in os.listdir(data_folder):
    file_path = os.path.join(data_folder, file_name)

    # skip if not a file (e.g., subfolder)
    if not os.path.isfile(file_path):
        continue

    ext = os.path.splitext(file_name)[1].lower()
    if ext not in allowed_exts:
        # skip unsupported formats
        continue

    print("\nProcessing =>", file_path)

    # SELECT LOADER BY EXTENSION
    if ext == ".pdf":
        loader = PDFPlumberLoader(file_path)

    elif ext == ".docx":
        loader = Docx2txtLoader(file_path)

    elif ext == ".html":
        loader = UnstructuredHTMLLoader(file_path)

    elif ext == ".txt":
        loader = TextLoader(file_path, encoding="utf-8")

    else:
        # safety (should not reach here because of allowed_exts)
        continue

    # LOAD & SPLIT
    docs = loader.load()
    chunks = splitter.split_documents(docs)

    output = []
    for i, c in enumerate(chunks):
        text = c.page_content.strip()
        if not text:
            continue

        vec = embedder.embed_query(text)

        output.append({
            "id": i,
            "text": text,
            "embedding": vec
        })

    # SAVE 1 JSON PER FILE
    safe_name = file_name.replace(" ", "_")
    outname = f"embeddings_{safe_name}.json"

    with open(outname, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)

    print("✔ Saved:", outname)

print("\nDONE.")
