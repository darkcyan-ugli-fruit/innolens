# Usage: PYTHONPATH=src python src/core/key_words_extractor.py

import os
from dotenv import load_dotenv
from openai import OpenAI as OpenAIClient  # Rename for clarity
from openai.types.responses import Response
import json
from utils.openai_utils import load_openai_client

OPENAI_MODEL = "gpt-4o-mini"

def extract_search_terms(research_objective: str,
                         client: OpenAIClient = load_openai_client(),
                         model: str = OPENAI_MODEL
                         )-> dict:

    # Prompt instruction to get the key words
    prompt: str = f"""
    You are assisting a researcher in gener,ating targeted search terms for academic and patent literature related to the research topic described below.

    Return a JSON object with the following structure:
    - "main_topic": a concise list with one element of words (2–3 words) in singular, extracted from the Research Objective that reflects the core technological focus
    - "secondary_topic": exactly 5 single word search terms, extracted from the Research Objective that reflects the client objective
    
    Instructions:
    - Output must be valid JSON only — no markdown, comments, or extra text
    - All terms in "secondary_topic" must be single word
    - Do NOT include any words or close variants from "main_topic" in "secondary_topic"
    - All terms across the fields must be unique — no repetition or synonyms
    - Each term in "secondary_topic" must be conceptually compatible with the "main_topic" so that combining them (e.g. "main_topic" AND "keyword") produces a realistic and meaningful research query
    - Use language and terminology commonly found in scientific publications and patent documents

    Research Objective:
    \"\"\" 
    {research_objective} 
    \"\"\"
    """
        
    response: Response = client.responses.create(

        model=model, # Availables models: https://platform.openai.com/docs/pricing
        input = prompt
    )

    print(f"The lenght of research objective is: {len(research_objective)}")
   
    research_key_words: dict[str, list[str]]= json.loads(response.output_text)
    
    print(research_key_words)

    return research_key_words


# For standalone testing
if __name__ == "__main__":
            
    # Research objective
    CLIENT_OBJECTIVE: str = """
    At present, one of our clients is looking to speak with professionals who have insights about the emerging technologies 
    in soft contact lens manufacturing, particularly non-injection moulded methods. They would broadly like to understand how 
    these technologies are reshaping the industry—from on-demand manufacturing to smart, drug-delivery-enabled lenses.
    """
    search_terms_dict = extract_search_terms(CLIENT_OBJECTIVE)