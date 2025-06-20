import streamlit as st
from core.openalex_pipeline import run_openalex_pipeline

def run_openalex_step():
    search_terms = st.session_state.final_keywords
    main_topic = search_terms["main_topic"][0]
    secondary = search_terms["secondary_topic"]

    st.subheader("📚 OpenAlex Search Results")
    with st.spinner("Querying OpenAlex..."):
        df = run_openalex_pipeline(main_topic, secondary)
        if df is not None:
            st.success(f"Fetched {len(df)} papers.")
            st.dataframe(df)
        else:
            st.warning("No results returned from OpenAlex.")
