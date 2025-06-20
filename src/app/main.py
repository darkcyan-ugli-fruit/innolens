# Usage: PYTHONPATH=src streamlit run src/app/main.py

import streamlit as st
from app.ui import keyword_extraction, keyword_review, keyword_display

from app.ui import (
    keyword_extraction,
    keyword_review,
    keyword_display,
    openalex_results,
    patentview_results,
    fda_results
)

st.set_page_config(page_title="Innolens MVP", layout="wide")
st.title("Innolens — Contact Lens Technology Scouting")

# Initialize session state
for var in ['search_terms', 'final_keywords']:
    if var not in st.session_state:
        st.session_state[var] = None

# Step 1: Keyword extraction pipeline
keyword_extraction.run_keyword_extraction()
keyword_review.run_keyword_review()
keyword_display.display_final_keywords()

# Step 2 (optional): Allow toggling additional pipelines
if st.session_state.final_keywords:
    with st.expander("Run Pipelines"):
        if st.checkbox("Run PatentView Search"):            
            patentview_results.run_patentview_step()
        
        if st.checkbox("Run FDA Pipeline"):
            fda_results.run_fda_step()
        
        if st.checkbox("Run Openalex Pipeline"):
            openalex_results.run_openalex_step()