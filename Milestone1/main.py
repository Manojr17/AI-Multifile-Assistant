import os
from langchain_community.document_loaders import (
    PDFPlumberLoader,
    Docx2txtLoader,
    TextLoader,
    UnstructuredHTMLLoader
)

# --------------------- CONFIG ---------------------
DATA_FOLDER = "../data"                   # Folder containing your 4 files
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
