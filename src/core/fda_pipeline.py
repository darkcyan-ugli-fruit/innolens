# PYTHONPATH=src python src/core/fda_pipeline.py

import requests
import pandas as pd
import time
import json
from typing import Any
from dotenv import load_dotenv

from config.fda_config import FDA_BASE_URL, FDA_LIMIT
from utils.nested_json import safe_get
from utils.pandas_utils import check_and_remove_duplicates, missing_report

import requests
import pandas as pd

def search_fda_510k(keyword: str, 
                    base_url: str = FDA_BASE_URL,
                    limit =FDA_LIMIT,
                    verbose: bool = False) -> pd.DataFrame:
    """
    Searches the FDA 510(k) database for devices matching the keyword.
    Returns a DataFrame with up to 1,000 results.
    """   
    # Query: wildcard match on keyword in device name and date range
    query: str = f'device_name:{keyword} AND decision_date:[1990-01-01 TO 2025-01-01]'
    
    params = {
        'search': query,
        'limit': limit
    }

    response: requests.Response = requests.get(base_url, params=params)
    
    response.raise_for_status()
    
    if response.status_code == 200:
        
        data: dict[str, Any] = response.json()
        results: list[dict[str, Any]] = data.get("results", [])
        
        if verbose:
            print("Type of data:", type(data))  # <class 'dict'>
            print("Type of 'results' field:", type(data.get("results")))  # list or None
            print("Pretty JSON:", json.dumps(data, indent=4))
        
        df = pd.DataFrame(results)
        df["main_keyword"] = keyword
        print(f"Found {len(df)} patents for '{keyword}'")
        return df
    else:
        print(f"Request failed with status {response.status_code}")
        return pd.DataFrame() 




# Entry point function for OpenAlex pipeline
def run_fda_pipeline(search_terms_dict: dict[str, list[str]]) -> pd.DataFrame:
    """
    Main pipeline entry: fetch OpenAlex data based on search terms.
    """
    main_topic=search_terms_dict["main_topic"][0]
    secondary_keywords=search_terms_dict["secondary_topic"]
    
    # SECTION 1: RESEARCH QUERY
    # Run the FDA search
    df: pd.DataFrame = search_fda_510k(main_topic, verbose = False)
    
    # SECTION 2: DATAFRAME CLEANING
    # Step 1: remove duplicated rows
    df: pd.DataFrame =  check_and_remove_duplicates(df, col="k_number")
    # Keep selected columsn
    df: pd.DataFrame = df[['device_name', 'applicant', 'decision_date', 'k_number', 'decision_description', 'contact', 'product_code','country_code']].copy()

    # convert to datetime
    df ['decision_date'] = pd.to_datetime(df ['decision_date'])

    print(df .dtypes)
    
    # SECTION 3: Filter by product code
    fda_product_code_df = pd.read_excel("data/no_careproducts_PCDExcelReport26.xls", sheet_name="Sheet1")
    print("The number of product code:", len(fda_product_code_df))
    
    # Extract the list of valid product codes
    valid_codes: list[str] = fda_product_code_df["Product Code"].astype(str).tolist()

    # Filter your main FDA DataFrame
    df: pd.DataFrame = df[df["product_code"].isin(valid_codes)].copy()

    # Inspect the result
    print(f"Rows before filtering: {len(df)}")
    print(f"Rows after filtering:  {len(df)}")
    
    # SECTION 4:Add code description
    desc_map = dict(
    zip(
        fda_product_code_df["Product Code"],
        fda_product_code_df["Device"]
        )
    )

    df.loc[:,"product_description"] = df["product_code"].map(desc_map)
    
    print("The unique product code:", df["product_code"].unique())

    
    return df


# Example usage block (for testing or CLI)
if __name__ == "__main__":
    search_terms_dict = {
        "main_topic": ["soft contact lens"],
        "secondary_topic": ['manufacturing', 'mold', 'injection', 'drug']
    }

    df = run_fda_pipeline(search_terms_dict)
    
    
    ####
    
    