import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

st.set_page_config(
    page_title="MLH Gemini RAG Playground",
    page_icon="https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Major_League_Hacking_logo.svg/1200px-Major_League_Hacking_logo.svg.png", # Using the MLH logo as icon
    layout="wide",
)

# Apply MLH Branding
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Open Sans', sans-serif;
        color: #353535;
    }

    h1, h3, h4, h5, h6 {
        font-family: 'Open Sans', sans-serif;
        font-weight: 700;
        color: #353535;
    }

    h2 {
        font-family: 'Open Sans', sans-serif;
        font-weight: 300;
        color: #353535;
    }

    .stButton > button {
        background-color: #C53C02;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
        font-weight: 600;
        transition: background-color 0.3s;
    }

    .stButton > button:hover {
        background-color: #751B00;
        color: white;
    }

    .stTextInput > div > div > input {
        border: 2px solid #265A8F;
        border-radius: 5px;
        color: #353535;
    }

    /* Streamlit specific overrides */
    div[data-testid="stToolbar"] {
        visibility: hidden;
    }

    .reportview-container .main .block-container{
        padding-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.logo("https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Major_League_Hacking_logo.svg/1200px-Major_League_Hacking_logo.svg.png")

st.title("Major League Hacking (MLH) Gemini RAG Playground")

# Initialize client
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("GEMINI_API_KEY environment variable not set. Please check your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)

# User input
query = st.text_input("Ask a question about the docs:", "In one sentence, explain the relationship between Major League Hacking and DEV.to")

if st.button("Submit"):
    if not query:
        st.warning("Please enter a query.")
    else:
        with st.spinner("Generating answer..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=query,
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

                st.subheader("Answer")
                st.write(response.text)

                st.subheader("Citations")
                if response.candidates and response.candidates[0].grounding_metadata:
                    # Displaying the grounding metadata as JSON
                    # Using str() or vars() depending on the object structure if to_dict() isn't available,
                    # but typically response objects might be pydantic models or similar.
                    # Streamlit handles dictionaries well.
                    # Let's try to convert it to a compatible format if needed
                    st.write(response.candidates[0].grounding_metadata)
                else:
                    st.write("No citations available.")

            except Exception as e:
                st.error(f"An error occurred: {e}")
