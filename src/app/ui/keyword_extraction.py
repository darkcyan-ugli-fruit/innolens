# src/app/ui/keyword_extraction.py

import streamlit as st
from core.key_words_extractor import extract_search_terms

def run_keyword_extraction():
    st.header("Step 1 — Extract Keywords")

    research_objective = st.text_area("Enter the research objective:", height=200)

    if st.button("Extract Keywords"):
        if not research_objective:
            st.warning("Please enter a research objective first.")
        else:
            search_terms = extract_search_terms(research_objective)
            st.session_state.search_terms = search_terms
            st.session_state.final_keywords = None
            st.session_state.research_objective = research_objective
            st.success("Keywords extracted and stored in session state.")


