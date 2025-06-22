import streamlit as st

# Load API key from Streamlit secrets
PATENTVIEW_API_KEY: str = st.secrets.get("PATENTSVIEW_API_KEY")

# Define the number of results returned per request
PATENTVIEW_SIZE: int = 1000

# Endpoint and headers
PATENTVIEW_URL: str = "https://search.patentsview.org/api/v1/patent"
PATENTVIEW_HEADERS: dict[str, str] = {
    "X-Api-Key": PATENTVIEW_API_KEY,
    "Content-Type": "application/json"
}


# --- load key with .env ---
# from dotenv import load_dotenv
# import os

# # Load API key
# load_dotenv()

# PATENTVIEW_API_KEY: str = os.getenv("PATENTSVIEW_API_KEY")

# # Define the number of results retuiurned per request
# PATENTVIEW_SIZE: int = 1000

# # Endpoint and headers
# PATENTVIEW_URL: str = "https://search.patentsview.org/api/v1/patent" # url = "https://search.patentsview.org/api/v1/patent"
# PATENTVIEW_HEADERS: dict[str, str] = {
#     "X-Api-Key": PATENTVIEW_API_KEY,
#     "Content-Type": "application/json"
# }