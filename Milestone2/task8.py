import os
from dotenv import load_dotenv

from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore

from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain

from prompt_template import SYSTEM_TEMPLATE

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "milestone-index"

# Embedding model (same as used while indexing)
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load existing Pinecone index
vector_store = PineconeVectorStore.from_existing_index(
    embedding=embedding,
    index_name=index_name
)

# Retriever
retriever = vector_store.as_retriever(search_kwargs={"k": 5})

# Prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_TEMPLATE),
    ("human", "Context:\n{context}\n\nQuestion: {input}")
])

# LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0
)

# Document chain
doc_chain = create_stuff_documents_chain(
    llm=llm,
    prompt=prompt
)

# Retrieval chain (RAG)
rag_chain = create_retrieval_chain(
    retriever,
    doc_chain
)

# User Query
if __name__ == "__main__":
    print("RAG chain loaded successfully.")
    
    query = input("Enter your query: ")
    # Invoke the RAG chain with multiple fallback call patterns to handle different LangChain versions.
    try:
        # Preferred simple API
        result = rag_chain.run(query)
        if isinstance(result, str):
            answer = result
        elif isinstance(result, dict):
            answer = result.get("answer") or result.get("output_text") or str(result)
        else:
            answer = str(result)
    except Exception:
        try:
            result = rag_chain.invoke({"input": query})
            if isinstance(result, dict):
                answer = result.get("answer") or result.get("output_text") or str(result)
            else:
                answer = str(result)
        except Exception:
            try:
                result = rag_chain({"input": query})
                if isinstance(result, dict):
                    answer = result.get("answer") or result.get("output_text") or str(result)
                else:
                    answer = str(result)
            except Exception as e:
                answer = f"Error invoking RAG chain: {e}"

    print("\nResponse:\n")
    print(answer)
