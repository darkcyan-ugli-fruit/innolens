import pandas as pd

def check_and_remove_duplicates(df: pd.DataFrame, col: str) -> pd.DataFrame:

    print("Dirty dataframe shape:", df.shape)
    duplicates: pd.DataFrame = df[df.duplicated(subset=col, keep=False)]

    if not duplicates.empty:
        print(f"\nFound {duplicates.shape[0]} duplicate rows based on column '{col}':")
        # print(duplicates)
        df_cleaned: pd.DataFrame = df.drop_duplicates(subset=col, keep="first").reset_index(drop=True)
        print(f"\n Removed duplicates. New dataframe shape: {df_cleaned.shape}")
        return df_cleaned
    else:
        print(f"\nNo duplicates found in '{col}'.")
        print(f"The dataframe shape is {df.shape}")
        return df
    
def missing_report(df: pd.DataFrame, column_name: str)-> None:
    """
    Print total rows, missing count, and percentage missing for a given column.
    """
    total_rows: int = len(df)
    missing_count: int = df[column_name].isna().sum()
    percent_missing: int = (missing_count / total_rows) * 100

    print(f"Column: {column_name}")
    print(f"Total rows: {total_rows}")
    print(f"Missing: {missing_count}")
    print(f"Percentage missing: {percent_missing:.2f}%")
    
