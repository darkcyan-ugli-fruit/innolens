import pandas as pd
import matplotlib.pyplot as plt

# --- FDA TRENDS ---
def plot_fda_submissions_over_time(fda_df: pd.DataFrame) -> plt.Figure:
    
    """
    Returns a Matplotlib figure showing FDA 510(k) submissions per year.
    """
    df = fda_df.copy()
    df['decision_date'] = pd.to_datetime(df['decision_date'], errors='coerce')
    df['decision_year'] = df['decision_date'].dt.year

    yearly = (
        df
        .groupby('decision_year')
        .size()
        .reset_index(name='count')
        .dropna(subset=['decision_year'])
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(yearly['decision_year'], yearly['count'], marker='o')
    ax.set_title('FDA 510(k) Submissions per Year', fontsize=16)
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Submissions')
    ax.grid(True)
    plt.tight_layout()

    return fig

def plot_top_fda_applicants(
    fda_df: pd.DataFrame,
    top_n: int = 10,
    show_inline: bool = False
) -> plt.Figure:
    """
    Plots the top N FDA 510(k) applicants (cleaned) as a horizontal bar chart.

    """
    # Copy to avoid mutating original
    df = fda_df.copy()

    # Count submissions per applicant
    top_applicants = (
        df['applicant_standardized']
        .value_counts()
        .head(top_n)
    )

    # Build the figure
    fig, ax = plt.subplots(figsize=(10, 6))
    top_applicants.plot(kind='barh', ax=ax)
    ax.set_xlabel("Number of 510(k) Submissions", fontsize=14)
    ax.set_ylabel("Applicant", fontsize=14)
    ax.set_title(f"Top {top_n} FDA 510(k) Applicants (Cleaned)", fontsize=16)
    ax.invert_yaxis()  # highest at top
    plt.tight_layout()

    # Show inline in notebooks
    if show_inline:
        plt.show()

    return fig

def plot_fda_approvals_by_product_code(
    fda_df: pd.DataFrame,
    show_inline: bool = False
) -> plt.Figure:
    """
    Plots a stacked bar chart of FDA device approvals per year, broken out by product code.

    """
    # 1. Prepare data
    df = fda_df.copy()
    df['decision_date'] = pd.to_datetime(df['decision_date'], errors='coerce')
    df['decision_year'] = df['decision_date'].dt.year

    # 2. Group by year and product code
    product_year_trend = (
        df
        .groupby(['decision_year', 'product_code'])
        .size()
        .unstack(fill_value=0)
    )

    # 3. Plot
    fig, ax = plt.subplots(figsize=(12, 6))
    product_year_trend.plot(
        kind='bar',
        stacked=True,
        colormap='tab20',
        ax=ax
    )

    # 4. Decorations
    ax.set_title("FDA Device Approvals by Product Code per Year", fontsize=16)
    ax.set_xlabel("Year", fontsize=14)
    ax.set_ylabel("Number of Approvals", fontsize=14)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    ax.legend(
        title="Product Code",
        bbox_to_anchor=(1.02, 1),
        loc='upper left',
        fontsize='small'
    )
    plt.tight_layout()

    # 6. Show inline for notebooks
    if show_inline:
        plt.show()

    return fig

# --- PATENTS TRENDS ---
def plot_patent_trend_common_companies(
    patentview_df: pd.DataFrame,
    common_companies: set[str],
    show_inline: bool = False
) -> plt.Figure:
    """
    Plots number of patents per year for companies found in both FDA and PatentView datasets.

    """
    # 1. Filter relevant patents
    filtered_patentview = patentview_df[
        patentview_df['assignee_standardized'].isin(common_companies)
    ]

    # 2. Count patents per year
    yearly_counts = filtered_patentview.groupby('year').size()

    # 3. Plot
    fig, ax = plt.subplots(figsize=(12, 6))
    yearly_counts.plot(kind='bar', color='skyblue', ax=ax)

    ax.set_title('Patent Activity Over Time (Common Companies)', fontsize=16)
    ax.set_xlabel('Year', fontsize=14)
    ax.set_ylabel('Number of Patents', fontsize=14)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()

    if show_inline:
        plt.show()

    return fig

def plot_fda_trend_common_companies(
    fda_df: pd.DataFrame,
    common_companies: set[str],
    show_inline: bool = False
) -> plt.Figure:
    """
    Plots the number of FDA 510(k) submissions per year for companies 
    found in both FDA and PatentView datasets.

    """
    # 1. Filter to common companies
    filtered_fda = fda_df[fda_df['applicant_standardized'].isin(common_companies)]

    # 2. Group and count by year
    yearly_counts = filtered_fda.groupby('year').size()

    # 3. Plot
    fig, ax = plt.subplots(figsize=(12, 6))
    yearly_counts.plot(kind='bar', color='lightgreen', ax=ax)

    ax.set_title('FDA Submission Activity Over Time (Common Companies)', fontsize=16)
    ax.set_xlabel('Year', fontsize=14)
    ax.set_ylabel('Number of Submissions', fontsize=14)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()

    if show_inline:
        plt.show()

    return fig

# --- OPENALEX TRENDS ---
def plot_papers_per_year_by_keyword(
    df: pd.DataFrame,
    show_inline: bool = False
) -> plt.Figure:
    """
    Creates a stacked bar chart showing the number of papers published per year,
    grouped by keyword. Returns the matplotlib Figure object.
    """
    # Make a copy to avoid mutating the original DataFrame
    data = df.copy()

    # Step 1: Group the data by year and keyword, count occurrences
    grouped_data = (
        data
        .groupby(['year', 'keyword'])
        .size()
        .unstack(fill_value=0)
    )

    # Step 2: Create a figure & axes
    fig, ax = plt.subplots(figsize=(12, 7))

    # Step 3: Plot the stacked bar chart
    grouped_data.plot(
        kind='bar',
        stacked=True,
        ax=ax
    )

    # Step 4: Add titles and axis labels
    ax.set_title('Number of Papers by Year and Keyword (Stacked)', fontsize=16)
    ax.set_xlabel('Year', fontsize=14)
    ax.set_ylabel('Number of Papers', fontsize=14)

    # Step 5: Format x-axis labels and legend
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.legend(title='Keyword', fontsize=10)

    # Step 6: Adjust layout
    plt.tight_layout()

    # Step 7: Show inline if requested
    if show_inline:
        plt.show()

    # Return the figure for Streamlit (or further use)
    return fig

def plot_top_institutions(
    df: pd.DataFrame,
    top_n: int = 10,
    show_inline: bool = False
) -> plt.Figure:
    """
    Plots a horizontal bar chart of the top institutions by number of papers.
    """
    # Copy to avoid mutating original
    data = df.copy()

    # Step 1: Count papers per institution
    institution_counts = data['institution_display_name'].value_counts().head(top_n)

    # Step 2: Create figure and axes
    fig, ax = plt.subplots(figsize=(12, 7))

    # Step 3: Plot horizontal bar chart
    institution_counts.plot(kind='barh', ax=ax, color='skyblue')

    # Step 4: Add titles and labels
    ax.set_title(f'Top {top_n} Institutions by Number of Papers', fontsize=16)
    ax.set_xlabel('Number of Papers', fontsize=14)
    ax.set_ylabel('Institution', fontsize=14)

    # Step 5: Invert y-axis to have highest value on top
    ax.invert_yaxis()

    # Step 6: Adjust layout
    plt.tight_layout()

    # Step 7: Show inline in notebooks if requested
    if show_inline:
        plt.show()

    return fig

def plot_top_last_authors(
    df: pd.DataFrame,
    top_n: int = 10,
    show_inline: bool = False
) -> plt.Figure:
    """
    Plots a horizontal bar chart of the top last authors by number of papers.

    """
    # Copy to avoid mutating original DataFrame
    data = df.copy()

    # Step 1: Count papers per last author
    last_author_counts = data['last_author_display_name'].value_counts().head(top_n)

    # Step 2: Create figure and axes
    fig, ax = plt.subplots(figsize=(12, 7))

    # Step 3: Plot horizontal bar chart
    last_author_counts.plot(kind='barh', ax=ax, color='skyblue')

    # Step 4: Add titles and labels
    ax.set_title(f'Top {top_n} Last Authors by Number of Papers', fontsize=16)
    ax.set_xlabel('Number of Papers', fontsize=14)
    ax.set_ylabel('Last Author', fontsize=14)

    # Step 5: Invert y-axis to have highest values at the top
    ax.invert_yaxis()

    # Step 6: Adjust layout
    plt.tight_layout()

    # Step 7: Show inline in notebooks if requested
    if show_inline:
        plt.show()

    return fig

def plot_top_countries_by_institution(
    df: pd.DataFrame,
    top_n: int = 10,
    show_inline: bool = False
) -> plt.Figure:
    """
    Creates a horizontal bar chart of the top countries by number of papers
    using the 'institution_country_code' column.
    """
    data = df.copy()

    if 'institution_country_code' not in data.columns:
        raise ValueError("Column 'institution_country_code' not found in the DataFrame.")

    # Count papers by country
    counts = data['institution_country_code'].value_counts().head(top_n)

    # Plot
    fig, ax = plt.subplots(figsize=(12, 7))
    counts.plot(kind='barh', ax=ax, color='lightgreen')

    ax.set_title(f"Top {top_n} Countries by Number of Papers", fontsize=16)
    ax.set_xlabel("Number of Papers", fontsize=14)
    ax.set_ylabel("Country Code", fontsize=14)
    ax.invert_yaxis()
    plt.tight_layout()

    if show_inline:
        plt.show()

    return fig