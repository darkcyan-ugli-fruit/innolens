# PYTHONPATH=src python src/core/openalex_pipeline.py


import pandas as pd
from core.openalex_query import fetch_openalex_data
from utils.nested_json import safe_get

def openalex_filter_col(df: pd.DataFrame)->pd.DataFrame:

    # print(df.columns.tolist())
    openalex_columns_to_keep: list[str] = ["keyword","title", "publication_date", "authorships", "abstract_inverted_index"]
    filtered_df: pd.DataFrame = df[openalex_columns_to_keep].copy()
    
    return filtered_df   

# Entry point function for OpenAlex pipeline
def run_openalex_pipeline(main_topic: str, secondary_keywords: list[str], verbose: bool = False) -> pd.DataFrame:
    """
    Main pipeline entry: fetch OpenAlex data based on search terms.
    """
    df = fetch_openalex_data(
        main_topic=main_topic,
        secondary_keywords=secondary_keywords,
        verbose=verbose
    )
    df = openalex_filter_col(df)
    
    # Data extraction logic

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
    return df


# Example usage block (for testing or CLI)
if __name__ == "__main__":
    search_terms_dict = {
        "main_topic": "soft contact lens",
        "secondary_topic": ["drug", "mold"]
    }

    df = run_openalex_pipeline(
        main_topic=search_terms_dict["main_topic"],
        secondary_keywords=search_terms_dict["secondary_topic"]
    )
    