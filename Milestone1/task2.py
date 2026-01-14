import os
from langchain_community.document_loaders import (
    PDFPlumberLoader,
    Docx2txtLoader,
    TextLoader,
    UnstructuredHTMLLoader
)

# --------------------- CONFIG ---------------------
DATA_FOLDER = "../data"               # Folder containing your 4 files
OUTPUT_FILE = "combined_text.txt"         # Final output text file


# --------------------- LOAD FILE FUNCTION ---------------------
def load_file(file_path):
    ext = file_path.lower()

    if ext.endswith(".pdf"):
        loader = PDFPlumberLoader(file_path)

    elif ext.endswith(".docx"):
        loader = Docx2txtLoader(file_path)

    elif ext.endswith(".txt"):
        loader = TextLoader(file_path, encoding="utf-8")  # FIX: UTF-8

    elif ext.endswith(".html") or ext.endswith(".htm"):
        loader = UnstructuredHTMLLoader(file_path)        # CLEAN OUTPUT

    else:
        print(f"❌ Unsupported file type: {file_path}")
        return []

    print(f"🔄 Loading file: {os.path.basename(file_path)}")
    return loader.load()


# --------------------- MAIN SCRIPT ---------------------
def main():
    all_text = ""

    for filename in os.listdir(DATA_FOLDER):
        file_path = os.path.join(DATA_FOLDER, filename)

        if os.path.isfile(file_path):
            docs = load_file(file_path)

            for doc in docs:
                if doc.page_content:
                    all_text += doc.page_content.strip() + "\n\n"

    # Save combined text
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(all_text)

    print("\n🎉 DONE! Clean combined text saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()


# --------------------- CHUNKING PART ---------------------

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document  # <-- FIXED IMPORT

CHUNK_SIZE = 2000
CHUNK_OVERLAP = int(CHUNK_SIZE * 0.10)   
CHUNK_OUTPUT = "chunked_output.txt"

def create_chunks():
    # Read the combined raw text
    with open("combined_text.txt", "r", encoding="utf-8") as f:
        full_text = f.read()

    # Convert into a LangChain Document
    docs = [Document(page_content=full_text)]

    # Create splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = splitter.split_documents(docs)

    # Write chunks to file
    with open(CHUNK_OUTPUT, "w", encoding="utf-8") as f:
        for i, chunk in enumerate(chunks):
            f.write(f"----- Chunk {i+1} -----\n")
            f.write(chunk.page_content.strip())
            f.write("\n\n")

    print(f"🎯 Created {len(chunks)} chunks!")
    print(f"📄 Chunked text saved to: {CHUNK_OUTPUT}")


# Run chunking after main()
create_chunks()
