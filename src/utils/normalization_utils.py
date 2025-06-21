import pandas as pd
import json
from openai.types.responses import Response
from utils.openai_utils import load_openai_client, OPENAI_MODEL

def normalize_company_names(
    patentview_df: pd.DataFrame,
    fda_df: pd.DataFrame,
    verbose: bool = False
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Normalizes organization names in PatentView and FDA DataFrames to parent company names via OpenAI.
    Adds 'assignee_standardized' and 'applicant_standardized' columns.

    Args:
        patentview_df (pd.DataFrame): Patent data with 'assignee_organization'.
        fda_df (pd.DataFrame): FDA data with 'applicant'.
        verbose (bool): If True, prints the name mapping.

    Returns:
        Tuple of updated (patentview_df, fda_df)
    """
    # 1. Combine and deduplicate company names
    company_names = pd.concat([
        patentview_df['assignee_organization'],
        fda_df['applicant']
    ]).dropna().unique().tolist()

    name_list = '\n'.join(company_names)

    # 2. Prompt for OpenAI
    prompt = f"""
    System:
    You are a company-name–normalization expert. Your job is to map raw, potentially messy organization names to their canonical parent company names.

    User:
    I have the following list of company names (one per line), which may include subsidiaries, legal suffixes (Inc, LLC, GmbH, etc.), or spelling variants:

    {name_list}

    Task:
    1. For each original name, determine the standardized parent company name.
    2. If the name is already the parent, map it to itself.
    3. Strip off any legal suffixes in the output (e.g. “Inc”, “LLC”, “GmbH”).
    4. Use the most common / widely recognized parent name.

    Output:
    - Return **only** a single JSON object.
    - Keys must be the **exact** original names.
    - Values must be the cleaned parent names.
    - Do **not** include any markdown, comments, or extra fields—just valid JSON.
    """

    # 3. Send to OpenAI
    try:
        client = load_openai_client()
        response: Response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.choices[0].message.content.strip()
        mapping = json.loads(content)
    except Exception as e:
        print(f"[OpenAI error] Failed to normalize company names: {e}")
        return patentview_df, fda_df

    if verbose:
        print("🔁 Name Mapping:")
        print(json.dumps(mapping, indent=2))

    # 4. Apply mappings
    patentview_df = patentview_df.copy()
    fda_df = fda_df.copy()

    patentview_df['assignee_standardized'] = patentview_df['assignee_organization']
    fda_df['applicant_standardized'] = fda_df['applicant']

    if 'assignee_organization' in patentview_df.columns:
        mask_pv = patentview_df['assignee_organization'].isin(mapping)
        patentview_df.loc[mask_pv, 'assignee_standardized'] = (
            patentview_df.loc[mask_pv, 'assignee_organization'].map(mapping)
        )

    if 'applicant' in fda_df.columns:
        mask_fda = fda_df['applicant'].isin(mapping)
        fda_df.loc[mask_fda, 'applicant_standardized'] = (
            fda_df.loc[mask_fda, 'applicant'].map(mapping)
        )

    return patentview_df, fda_df

def find_common_companies(patentview_df: pd.DataFrame, fda_df: pd.DataFrame, verbose: bool = True) -> set[str]:
    """
    Find companies that appear in both the FDA and PatentView datasets based on standardized names.
    """
    # Get unique standardized company names from each dataset
    patent_companies = set(patentview_df['assignee_standardized'].dropna().unique())
    fda_companies = set(fda_df['applicant_standardized'].dropna().unique())

    # Find intersection
    common_companies = patent_companies.intersection(fda_companies)

    # Optionally print the results
    if verbose:
        print(f"Number of companies in both datasets: {len(common_companies)}")
        print("Companies found in both FDA and PatentView:")
        for company in sorted(common_companies):
            print(company)

    return common_companies

