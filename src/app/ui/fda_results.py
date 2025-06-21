import streamlit as st
from core.fda_pipeline import run_fda_pipeline

def run_fda_step():
    search_terms = st.session_state.final_keywords
    main_topic = search_terms["main_topic"][0]
    secondary = search_terms["secondary_topic"]

    st.subheader("💊 FDA Results")

    # Only run if not already in session_state
    if "fda_df" not in st.session_state:
        with st.spinner("Querying FDA Database..."):
            fda_df = run_fda_pipeline(main_topic, secondary)
            st.session_state.fda_df = fda_df
    else:
        fda_df = st.session_state.fda_df

    if fda_df is not None:
        st.success(f"Fetched {len(fda_df)} FDA records.")
        st.write("Shape in Streamlit:", fda_df.shape)
        st.dataframe(fda_df)
    else:
        st.warning("No results returned from FDA API.")
