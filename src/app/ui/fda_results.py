import streamlit as st
from core.fda_pipeline import run_fda_pipeline

def run_fda_step():
    search_terms = st.session_state.final_keywords
    main_topic = search_terms["main_topic"][0]
    secondary = search_terms["secondary_topic"]

    st.subheader("💊 FDA Results")
    with st.spinner("Querying FDA Database..."):
        df = run_fda_pipeline(main_topic, secondary)
        if df is not None:
            st.success(f"Fetched {len(df)} FDA records.")
            st.dataframe(df)
        else:
            st.warning("No results returned from FDA API.")
