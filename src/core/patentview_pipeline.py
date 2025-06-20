# PYTHONPATH=src python src/core/patentview_pipeline.py

import requests
import pandas as pd
import time
import json
from typing import Any
from dotenv import load_dotenv

from config.patentview_config import PATENTVIEW_API_KEY, PATENTVIEW_SIZE, PATENTVIEW_URL, PATENTVIEW_HEADERS
from utils.nested_json import safe_get
from utils.pandas_utils import check_and_remove_duplicates, missing_report
# from utils.openai_utils import load_openai_client



# # Load API key
# load_dotenv()

def fetch_patentview_data(search_term: str,
                          url: str = PATENTVIEW_URL,
                          headers: dict[str, str] = PATENTVIEW_HEADERS,
                          size: int = PATENTVIEW_SIZE, # specifies the number of results per page
                          verbose: bool = False
                          ) -> pd.DataFrame:
    """
    Search the PatentsView API for patents mentioning a term in the abstract.
    Returns a DataFrame with up to 1,000 records, including the keyword used.
    """

    query: dict[str, dict[str,str]] = {
        "_text_phrase": {
            "patent_abstract": search_term
        }
    }

    fields: list[str] = [
        "patent_id", "patent_title", "patent_date", "patent_abstract",
        "applicants", "application", "assignees", "attorneys", "cpc_current", 
    ]

    params: dict[str, str] = {
        "q": json.dumps(query),
        "f": json.dumps(fields),
        "o": json.dumps({"size": size}),
        "s": json.dumps([{"patent_date": "desc"}])
    }

    # Send a get request
    response: requests.Response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    
    if response.status_code == 200:
        
        data: dict[str, Any] = response.json()
        results: list[dict[str, Any]] = data.get("patents", [])
        
        if verbose:
            print("Type of data:", type(data))  # <class 'dict'>
            print("Type of 'results' field:", type(data.get("patents")))  # list or None
            print("Pretty JSON:", json.dumps(data, indent=4))
        
        df = pd.DataFrame(results)
        df["main_keyword"] = search_term
        print(f"Found {len(df)} patents for '{search_term}'")
        return df
    else:
        print(f"Request failed with status {response.status_code}")
        return pd.DataFrame()


# Entry point function for patentviw pipeline
def run_patentview_pipeline(main_topic: str, secondary_keywords: list[str]) -> pd.DataFrame:
    """
    Main pipeline entry: fetch patenview data based on search terms.
    """
    # main_topic=search_terms_dict["main_topic"][0]
    # secondary_keywords=search_terms_dict["secondary_topic"]
    
    # SECTION 1: RESEARCH QUERY
    # Fetche the patview data
    print("Fetching data started...")
    df = fetch_patentview_data(search_term = main_topic, verbose=False)
    print("Fetching is complete")

    # SECTION 2: DATA EXTRACTION LOGIC
    # Extract applicant_organization
    print("Extract data from nested object started..")
    df.loc[:, 'assignee_organization'] = df['assignees'].apply(
        lambda x: safe_get(x, [0, 'assignee_organization'])
    )

    # Extract first assignee_country
    df.loc[:, 'assignee_country'] = df['assignees'].apply(
        lambda x: safe_get(x, [0, 'assignee_country'])
    )

    # Extract cpc_group_id
    df.loc[:, 'cpc_group_id'] = df['cpc_current'].apply(
        lambda x: safe_get(x, [0, 'cpc_group_id'])
    )
    print("Extract data from nested object complete")
    
    # Create a new datafram
    df = df[['main_keyword',
             'patent_id', 
             'patent_title',
             'patent_date',
             'patent_abstract',
             #'applicants',
             'assignee_organization',
             'assignee_country',
             'cpc_group_id'
                ]].copy()

    print("Dataframe shape:",df.shape)
    missing_report(df, "assignee_organization")
    
    # SECTION 3: DATAFRAME CLEANING
    # remove duplicated rows
    df: pd.DataFrame =  check_and_remove_duplicates(df, col="patent_title")

    missing_report(df, "assignee_organization")
    
    # convert 'publication_date' column to datetime format
    df['patent_date'] = pd.to_datetime(df['patent_date'])

    # Extract the year and store it in a new column 'year'
    df['year'] = df['patent_date'].dt.year
    
    # SECTION 4: Add cooperative patent classification (cpc) description
    # Load the CPC title table
    cpc_titles: pd.DataFrame = pd.read_csv('data/g_cpc_title.tsv', sep='\t')
    cpc_titles.head()
    
    # Rename column in cpc_titles to match your patentview_df
    cpc_titles.rename(columns={'cpc_group': 'cpc_group_id'}, inplace=True)


   # create a mapping dic
    cpc_dict: dict[str, str] = dict(
        zip(
            cpc_titles['cpc_group_id'],
            cpc_titles['cpc_group_title']
        )
    )

    df.loc[:,'cpc_group_title'] = df['cpc_group_id'].map(cpc_dict)
    missing_report(df, "cpc_group_title")
    
    print("patentview dataframe final shape before reset:", df.shape)

    # Reset the index so it runs 0,1,2,…n-1
    df = df.reset_index(drop=True)

    print("patentview dataframe final shape after reset:", df.shape)
    
    return df


# Example usage block (for testing or CLI)
if __name__ == "__main__":
    search_terms_dict = {
        "main_topic": ["soft contact lens"],
        "secondary_topic": ['manufacturing', 'mold', 'injection', 'drug']
    }

    df = run_patentview_pipeline(main_topic = search_terms_dict["main_topic"][0], 
                               secondary_keywords= search_terms_dict["secondary_topic"] )
    
    
    
    ####
    
    