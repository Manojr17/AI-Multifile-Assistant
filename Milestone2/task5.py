from dotenv import load_dotenv
import os

# LOAD THE .ENV FILE FROM MILESTONE 1
load_dotenv(dotenv_path="../Milestone1/.env")

from langchain_openai import ChatOpenAI

# READ THE KEY
api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    api_key=api_key
)

response = llm.invoke("How to succeed in life")
print(response.content)
