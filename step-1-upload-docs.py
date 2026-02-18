import os
from dotenv import load_dotenv
from google import genai
import time

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

file_search_store = client.file_search_stores.create(config={'display_name': 'mlh-docs'})

print(f"Created file search store with name: {file_search_store.name}")

files = [
    "docs/mlh-hackathon-organizer-guide.txt",
    "docs/mlh-news.txt",
    "docs/mlh-policies.txt",
    "docs/mlh-hack-days.txt",
]

for file in files:
    operation = client.file_search_stores.upload_to_file_search_store(
        file=file,
        file_search_store_name=file_search_store.name,
        config={
            'display_name' : file.split('/')[-1],
        }
    )

    while not operation.done:
        time.sleep(2)
        operation = client.operations.get(operation)

    print(f"Finished uploading {file} to file search store")