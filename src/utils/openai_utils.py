# src/core/utils/openai_client.py

import os
from dotenv import load_dotenv
from openai import OpenAI as OpenAIClient

def load_openai_client() -> OpenAIClient:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables.")
    return OpenAIClient(api_key=api_key)
