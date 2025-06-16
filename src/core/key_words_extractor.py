import os
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.responses import Response
import json

# Load the API key
load_dotenv()

client: OpenAI = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_search_terms(research_objective: str)-> dict:


    # Prompt instruction to get the key words
    prompt: str = f"""
    You are assisting a researcher in generating targeted search terms for academic and patent literature related to the research topic described below.

    Return a JSON object with the following structure:
    - "main_topic": a concise list with one element of words (2–3 words) extracted from the Research Objective that reflects the core technological focus
    - "openalex": exactly 5 academic search terms, extracted from the Research Objective that reflects the client objective
    - "patentview": exactly 1 patent-related single keyword, not similar to maint topic, extrapolated from the Research Objective that reflects the general client objective
    - "cpc_codes": exactly 5 valid CPC classification codes relevant to the topic

    Instructions:
    - Output must be valid JSON only — no markdown, comments, or extra text
    - All terms in "openalex" and "patentview" must be single or double words
    - Do NOT include any words or close variants from "main_topic" in "openalex" or "patentview"
    - All terms across the fields must be unique — no repetition or synonyms
    - Each term in "openalex" and "patentview" must be conceptually compatible with the "main_topic" so that combining them (e.g. "main_topic" AND "keyword") produces a realistic and meaningful research query
    - Use language and terminology commonly found in scientific publications and patent documents

    Research Objective:
    \"\"\" 
    {research_objective} 
    \"\"\"
    """

    # Availables models: https://platform.openai.com/docs/pricing
    GPT_MODEL = "gpt-4o-mini"

    response: Response = client.responses.create(

        model=GPT_MODEL,
        input = prompt
    )

    print(f"The lenght of research objective is: {len(research_objective)}")
   
    research_key_words: list[str]= json.loads(response.output_text)
    
    print(research_key_words)

    return research_key_words


# For standalone testing
if __name__ == "__main__":
    # Research objective
    client_objective: str = """
    At present, one of our clients is looking to speak with professionals who have insights about the emerging technologies 
    in soft contact lens manufacturing, particularly non-injection moulded methods. They would broadly like to understand how 
    these technologies are reshaping the industry—from on-demand manufacturing to smart, drug-delivery-enabled lenses.
    """
    search_terms_json_response = extract_search_terms(client_objective)