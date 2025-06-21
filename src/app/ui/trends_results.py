import streamlit as st
from core.trends_analysis import (
    plot_fda_submissions_over_time,
    plot_top_fda_applicants,
    plot_fda_approvals_by_product_code,
    plot_patent_trend_common_companies,
    plot_fda_trend_common_companies,
    plot_papers_per_year_by_keyword,
    plot_top_institutions,
    plot_top_last_authors,
    plot_top_countries_by_institution,
)

# --- FDA Trends ---
def render_fda_trends():
    st.title("📈 FDA Trends")
    st.markdown("Visualizations based on FDA 510(k) data")

    fda_df = st.session_state.get("fda_df")

    if fda_df is not None:
        st.subheader("📅 Submissions per Year")
        st.pyplot(plot_fda_submissions_over_time(fda_df))

        st.subheader("🏢 Top FDA 510(k) Applicants")
        st.pyplot(plot_top_fda_applicants(fda_df, top_n=10))

        st.subheader("🔬 Approvals by Product Code")
        st.pyplot(plot_fda_approvals_by_product_code(fda_df))
    else:
        st.warning("⚠️ FDA data not found. Please run the FDA pipeline first.")

# --- PatentView Trends (Common Companies) ---
def render_patent_common_trends():
    st.title("🧠 PatentView Trends for Shared Companies")

    pv_df = st.session_state.get("patentview_df")
    fda_df = st.session_state.get("fda_df")
    common = st.session_state.get("common_companies")

    if pv_df is not None and fda_df is not None and common:
        st.subheader("📜 Patents Over Time (Shared Companies)")
        st.pyplot(plot_patent_trend_common_companies(pv_df, common))

        st.subheader("💊 FDA Submissions (Same Companies)")
        st.pyplot(plot_fda_trend_common_companies(fda_df, common))
    else:
        st.warning("⚠️ Run FDA + PatentView pipelines and normalization to enable shared trend plots.")

# --- OpenAlex Trends ---
def render_openalex_trends():
    st.title("📚 OpenAlex Trends")

    oa_df = st.session_state.get("openalex_df")

    if oa_df is not None and "year" in oa_df.columns and "keyword" in oa_df.columns:
        st.subheader("🗓️ Papers Per Year by Keyword")
        st.pyplot(plot_papers_per_year_by_keyword(oa_df))
        st.pyplot(plot_top_institutions(oa_df))
        st.pyplot(plot_top_last_authors(oa_df))
        st.pyplot(plot_top_countries_by_institution(oa_df))
    else:
        st.warning("⚠️ OpenAlex data not found or missing 'year'/'keyword' columns. Run the pipeline first.")
