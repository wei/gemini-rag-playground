import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

for document_in_store in client.file_search_stores.documents.list(parent='fileSearchStores/mlhdocs-nwpo11i0tbko'):
  print(document_in_store)
