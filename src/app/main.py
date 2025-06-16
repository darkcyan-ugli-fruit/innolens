# Usage: PYTHONPATH=src streamlit run src/app/main.py

import streamlit as st
from app.ui import keyword_extraction, keyword_review, keyword_display

st.set_page_config(page_title="Innolens MVP", layout="wide")
st.title("Innolens — Contact Lens Technology Scouting")

# Initialize session state
for var in ['search_terms', 'final_keywords']:
    if var not in st.session_state:
        st.session_state[var] = None

# Run pipeline modules
keyword_extraction.run_keyword_extraction()
keyword_review.run_keyword_review()
keyword_display.display_final_keywords()
