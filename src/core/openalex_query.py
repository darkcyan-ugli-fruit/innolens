# Constants
OPENALEX_URL:str = "https://api.openalex.org/works"
MAILTO: str = "adyl.elguamra@gmail.com"
OPENALEX_PER_PAGE: int = 50
PAGE: int = 1

import requests
import pandas as pd
import time
import json
from typing import Any


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

