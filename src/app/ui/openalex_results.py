import streamlit as st
from core.openalex_pipeline import run_openalex_pipeline

def run_openalex_step():
    search_terms = st.session_state.final_keywords
    main_topic = search_terms["main_topic"][0]
    secondary = search_terms["secondary_topic"]
    objective = st.session_state.research_objective  

    st.subheader("📚 OpenAlex Search Results")
    with st.spinner("Querying OpenAlex..."):
        openalex_df = run_openalex_pipeline(main_topic, secondary, objective) 
        st.write("Shape in Streamlit:", openalex_df.shape)
        if openalex_df is not None:
            st.success(f"Fetched {len(openalex_df)} papers.")
            st.dataframe(openalex_df)
        else:
            st.warning("No results returned from OpenAlex.")
