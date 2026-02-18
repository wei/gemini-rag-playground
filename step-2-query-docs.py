import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="In one sentence, explain the relationship between Major League Hacking and DEV.to",
    config=types.GenerateContentConfig(
        tools=[
            types.Tool(
                file_search=types.FileSearch(
                    file_search_store_names=["fileSearchStores/mlhdocs-nwpo11i0tbko"]
                )
            )
        ]
    )
)

print(response.text)