# PYTHONPATH=src python src/core/openalex_pipeline.py

import requests
import pandas as pd
import time
import json
from typing import Any
from openai import OpenAI as OpenAIClient
from openai.types.responses import Response

from config.openalex_config import OPENALEX_URL, MAILTO, OPENALEX_PER_PAGE, PAGE
from utils.nested_json import safe_get
from utils.pandas_utils import check_and_remove_duplicates, missing_report
from utils.openai_utils import load_openai_client



def openalex_query_api(
    query_result: str,
    url: str,
    keyword: str,
    headers: dict[str, str] | None,
    params: dict[str, str],
    verbose: bool = False
) -> list[dict]:
    """
    Sends a GET request to the OpenAlex API and returns the list of results.
    """
    try:
        response: requests.Response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data: dict[str, Any] = response.json()

        if verbose:
            print("Type of data:", type(data))  # <class 'dict'>
            print("Type of 'results' field:", type(data.get("results")))  # list or None
            print("Pretty JSON:", json.dumps(data, indent=4))

        return data.get(query_result, [])

    except requests.exceptions.RequestException as e:
        print(f"Error for keyword '{keyword}': {e}")
        return []

def fetch_openalex_data(
    main_topic: str,
    secondary_keywords: list[str],
    query_result: str = "results",
    url: str = OPENALEX_URL,
    mailto: str = MAILTO,
    per_page: int = OPENALEX_PER_PAGE,
    page: int = PAGE,
    delay: float = 1.0,
    verbose: bool = False
) -> pd.DataFrame | None:
    """
    Queries OpenAlex for each secondary keyword combined with the main topic,
    and returns a combined DataFrame of results.
    """
    dfs: list[pd.DataFrame] = []

    for kw in secondary_keywords:
        print(f"\nSearching for: '{main_topic} {kw}'")

        params: dict[str, str | int] = {
            "search": f"{main_topic} {kw}",
            "per_page": per_page,  # int
            "page": page,          # int
            "sort": "relevance_score:desc",
            "mailto": mailto
        }

        papers: list[dict] = openalex_query_api(
            query_result=query_result,
            url=url,
            keyword=kw,
            headers=None,
            params=params,
            verbose=verbose
        )

        if papers:
            df = pd.DataFrame(papers)
            df["keyword"] = kw
            dfs.append(df)

        time.sleep(delay)

    if dfs:
        result_df = pd.concat(dfs, ignore_index=True)
        print(f"Final DataFrame shape: {result_df.shape}")
        return result_df

    print("No results found.")
    return None

def openalex_filter_col(df: pd.DataFrame)->pd.DataFrame:

    print(df.columns.tolist())
    openalex_columns_to_keep: list[str] = ["keyword","title", "publication_date", "authorships", "abstract_inverted_index"]
    filtered_df: pd.DataFrame = df[openalex_columns_to_keep].copy()
    
    return filtered_df   

def reconstruct_abstract(abstract_inverted_index: dict[str, list[int]]) -> str:
    '''
    Reconstruct the abstract from abstract_inverted_index
    '''
    
    # Some works don't have an abstract
    if not abstract_inverted_index:
        return ""
        
    # Variable to store the highest index
    max_value: int = 0
     # Loop through all the list of position in the abstract_inverted_index dictionary.
    for values in abstract_inverted_index.values():
        # Loop through all the index value
        for value in values:
            # identify the highest value index
            if value >= max_value:
                max_value = value
                
    # Create an empty list with abstract size        
    abstract: list[str] = [None] * (max_value +1)

    # Loop through each word in the abstract_inverted_index:
    for word, positions in abstract_inverted_index.items():
        # For each word, get the list of positions it appears in.
        for position in positions:
            # Insert each word into its correct position in the list.
            abstract[position]= word
                        
    # Join all the words in the list into a single string, separated by spaces.
    # abstract_text: str = " ".join(abstract)
    abstract_text: str = " ".join(word if word is not None else "" for word in abstract)

    # print("\n", abstract_text)
    
    return abstract_text

def get_justification(title: str, abstract: str, objective:str)-> str:
    prompt = f"""
    You are the CEO, as well as a scientific and regulatory analyst, evaluating academic research for a company .

    Below is a paper's title and abstract, followed by the company's research objective. 
    
    Title:  
    {title}

    Abstract:  
    {abstract}

    Research Objective:  
    {objective}

    Assess if the paper is relevant. Start the answer with Yes or No, followed by a 1–2 sentence explanation based only on the title and abstract. 
    Be concise, specific, and fact-based. Avoid speculation or vague generalizations.
    """

    # print("Generating GPT justifications...")
    
    client: OpenAIClient = load_openai_client()
    
    try:
        response: Response = client.responses.create(
        model="gpt-4o-mini",
        input = prompt
        )
        return response.output_text
    except Exception as e:
        return f"ERROR: {e}"
    
def process_row(row: pd.Series, search_terms_dict: dict[str, list[str]]) -> pd.Series:
    output = get_justification(row["title"], row["abstract"], search_terms_dict)
    output_lower = output.lower()
    
    if output_lower.startswith("yes"):
        relevant = "yes"
    elif output_lower.startswith("no"):
        relevant = "no"
    else:
        relevant = "unclear"
        
    return pd.Series({"relevant": relevant, "justification": output})

# Entry point function for OpenAlex pipeline
def run_openalex_pipeline(search_terms_dict: dict[str, list[str]]) -> pd.DataFrame:
    """
    Main pipeline entry: fetch OpenAlex data based on search terms.
    """
    main_topic=search_terms_dict["main_topic"][0]
    secondary_keywords=search_terms_dict["secondary_topic"]
    
    print(main_topic)
    print(secondary_keywords)
    
    
    # SECTION 1: QUERY OPENALEX
    # Launch the paper search
    df = fetch_openalex_data(
        main_topic=main_topic,
        secondary_keywords=secondary_keywords
    )
    
    # FILTER RELEVANT DATA
    df: pd.DataFrame = openalex_filter_col(df)
    
    # SECTION 2:DATA EXTRACTION LOGIC
    print("Started the extraction: author_display_name...")
    df['first_author_display_name'] = df['authorships'].apply(
        lambda x: safe_get(x, [0, 'author', 'display_name'])
    )

    print("Started the extraction: last_author_display_name...")
    df['last_author_display_name'] = df['authorships'].apply(
        lambda x: safe_get(x, [1, 'author', 'display_name'])
    )

    print("Started the extraction: institution_display_name...")
    df['institution_display_name'] = df['authorships'].apply(
        lambda x: safe_get(x, [0, 'institutions', 0, 'display_name'])
    )

    print("Started the extraction: institution_country_code...")
    df['institution_country_code'] = df['authorships'].apply(
        lambda x: safe_get(x, [0, 'institutions', 0, 'country_code'])
    )
    
    # SECTION 3:ABSTRACT UTILITY
    # Extract abstrac: apply your reconstruct_abstract function
    print("Abtract extration started...")
    df.loc[:, 'abstract'] = df['abstract_inverted_index'].apply(reconstruct_abstract)
    print("Abtract extration complete.")
    
    # Create a new datafram
    df = df[['keyword', 
                                            'title',
                                            'abstract',
                                            'publication_date', 
                                            'first_author_display_name', 
                                            'last_author_display_name', 
                                            'institution_display_name', 
                                            'institution_country_code' 
                                            ]].copy()

    print(df.shape)   
    
    # SECTION 4: DATAFRAME CLEANING
    df = check_and_remove_duplicates(df, col="title")
    # Count None or NaN in 'applicant_organization' column
    none_count_openalex: int = df['institution_display_name'].isna().sum()
    print(f"Number of None/NaN values in 'applicant_organization' column: {none_count_openalex}")
    
    # IDENTIFY RELEVANT PAPERS
    # Create a new column: will inform if the paper is relevant or not
    df["relevant"] = ""
    # Create a new column: will provide the relevance justification
    df["justification"] = ""
    # print the shape
    print("Dataframe shape:",df.shape)
    # Print first rows of dataframe
    df[["title", "publication_date", "institution_country_code", "institution_display_name"]].head()
    
    # SECTION 5: IDENTIFY RELEVANT PAPERS
    # Apply the function to the entire DataFrame
    print("Started relevant paper identification...")
    df[["relevant", "justification"]] = df.apply(process_row, search_terms_dict)
    print("Relevant paper identification is complete")
    
    # Show full column contents and more columns
    #pd.set_option("display.max_colwidth", None)    # Show full text in cells
    print("The dataframe shape of all papers:", df.shape)

    # Filter relevant papers
    df: pd.DataFrame = df[df["relevant" == "Yes"]].copy()

    # Print shape
    print(f"The dataframe shape of relevant papers: {df.shape}")
    
    missing_report(df, "institution_display_name")
    
    # convert 'publication_date' column to datetime format
    df['publication_date'] = pd.to_datetime(df['publication_date'])

    # Extract the year and store it in a new column 'year'
    df['year'] = df['publication_date'].dt.year
    
    return None


# Example usage block (for testing or CLI)
if __name__ == "__main__":
    search_terms_dict = {
        "main_topic": ["soft contact lens"],
        "secondary_topic": ['manufacturing', 'mold', 'injection', 'drug']
    }

    df = run_openalex_pipeline(search_terms_dict)
    
    
    ####
    
    