import streamlit as st
from core.patentview_pipeline import run_patentview_pipeline

def run_patentview_step():
    search_terms = st.session_state.final_keywords
    main_topic = search_terms["main_topic"][0]
    secondary = search_terms["secondary_topic"]

    st.subheader("📄 PatentView Search Results")

    if "patentview_df" not in st.session_state:
        with st.spinner("Querying PatentView..."):
            patentview_df = run_patentview_pipeline(main_topic, secondary)
            st.session_state.patentview_df = patentview_df
    else:
        patentview_df = st.session_state.patentview_df

    if patentview_df is not None:
        st.success(f"Fetched {len(patentview_df)} patents.")
        st.write("Shape in Streamlit:", patentview_df.shape)
        st.dataframe(patentview_df)
    else:
        st.warning("No results returned from PatentView.")
