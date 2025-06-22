# Usage: streamlit run src/app/main.py

# src/app/main.py

import os
import sys

# ── Simple src/ path fix ──
# Treat innolens/src/ as a top-level import folder
cwd     = os.getcwd() # get the current working directory
src_dir = os.path.join(cwd, "src") # yields "/home/user/innolens/src
print(f"[DEBUG main.py] Inserting into sys.path: {src_dir}")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)
# ──────────────────────────

import streamlit as st
from utils.normalization_utils import normalize_company_names, find_common_companies

from app.ui import (
    keyword_extraction,
    keyword_review,
    keyword_display,
    openalex_results,
    patentview_results,
    fda_results,
    trends_results
)

st.set_page_config(page_title="Innolens MVP", layout="wide")
st.title("Innolens — Contact Lens Technology Scouting")

# Initialize session state
for var in ['search_terms', 'final_keywords']:
    if var not in st.session_state:
        st.session_state[var] = None

# --- Step 1: Keyword Workflow ---
with st.expander("Step 1: Keyword Workflow", expanded=True):
    keyword_extraction.run_keyword_extraction()
    keyword_review.run_keyword_review()
    keyword_display.display_final_keywords()

# --- Step 2: Run Pipelines ---
if st.session_state.final_keywords:
    with st.expander("Step 2: Run Data Pipelines"):
        if st.checkbox("Run PatentView Search"):
            patentview_results.run_patentview_step()

        if st.checkbox("Run FDA Pipeline"):
            fda_results.run_fda_step()

        if st.checkbox("Run OpenAlex Pipeline"):
            openalex_results.run_openalex_step()

# --- Step 3: Visualize Trends ---
with st.expander("Step 3: Visualize Trends"):
    has_data = (
        "fda_df" in st.session_state and st.session_state.fda_df is not None and
        "patentview_df" in st.session_state and st.session_state.patentview_df is not None
    )

    if has_data:
        # Normalize company names once
        if "normalized" not in st.session_state:
            st.info("🔄 Normalizing company names...")
            pv_df, fda_df = normalize_company_names(
                st.session_state.patentview_df,
                st.session_state.fda_df,
                verbose=True
            )
            st.session_state.patentview_df = pv_df
            st.session_state.fda_df = fda_df
            st.session_state.common_companies = find_common_companies(pv_df, fda_df, verbose=False)
            st.session_state.normalized = True

        # Trend visualizations
        if st.checkbox("📈 Show FDA Trends"):
            trends_results.render_fda_trends()

        if st.checkbox("🧠 Show PatentView Trends (Common Companies)"):
            trends_results.render_patent_common_trends()

        if st.checkbox("📚 Show OpenAlex Trends"):
            trends_results.render_openalex_trends()

    else:
        st.warning("⚠️ Please run both FDA and PatentView pipelines before viewing trends.")
