# src/core/utils/openai_client.py

import streamlit as st
from openai import OpenAI as OpenAIClient
from config.openai_config import OPENAI_API_KEY

OPENAI_MODEL = "gpt-4o-mini"

def load_openai_client() -> OpenAIClient:
    return OpenAIClient(api_key=OPENAI_API_KEY)

# --- load key with .env ---
# import os
# from dotenv import load_dotenv
# from openai import OpenAI as OpenAIClient

# OPENAI_MODEL = "gpt-4o-mini"

# def load_openai_client() -> OpenAIClient:
#     load_dotenv()
#     api_key = os.getenv("OPENAI_API_KEY")
#     if not api_key:
#         raise ValueError("OPENAI_API_KEY not found in environment variables.")
#     return OpenAIClient(api_key=api_key)

