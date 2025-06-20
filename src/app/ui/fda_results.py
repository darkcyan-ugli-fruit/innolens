import streamlit as st
from core.fda_pipeline import run_fda_pipeline

def run_fda_step():
    search_terms = st.session_state.final_keywords
    main_topic = search_terms["main_topic"][0]
    secondary = search_terms["secondary_topic"]

    st.subheader("💊 FDA Results")
    with st.spinner("Querying FDA Database..."):
        fda_df = run_fda_pipeline(main_topic, secondary)
        st.write("Shape in Streamlit:", fda_df.shape)
        
        if fda_df is not None:
            st.success(f"Fetched {len(fda_df)} FDA records.")
            st.dataframe(fda_df)
        else:
            st.warning("No results returned from FDA API.")
