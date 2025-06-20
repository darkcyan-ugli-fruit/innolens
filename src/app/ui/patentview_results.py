import streamlit as st
from core.patentview_pipeline import run_patentview_pipeline

def run_patentview_step():
    search_terms = st.session_state.final_keywords
    main_topic = search_terms["main_topic"][0]
    secondary = search_terms["secondary_topic"]

    st.subheader("📄 PatentView Search Results")
    with st.spinner("Querying PatentView..."):
        patenview_df = run_patentview_pipeline(main_topic, secondary)
        st.write("Shape in Streamlit:", patenview_df.shape)

        if patenview_df is not None:
            st.success(f"Fetched {len(patenview_df)} patents.")
            st.dataframe(patenview_df)
        else:
            st.warning("No results returned from PatentView.")
