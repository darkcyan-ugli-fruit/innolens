# src/app/ui/keyword_review.py

import streamlit as st

def run_keyword_review():
    if st.session_state.search_terms:
        st.header("Step 2 — Review Keywords & Manual Editing")

        search_terms = st.session_state.search_terms

        st.subheader("Main Topic")
        selected_main = st.multiselect(
            "Select main topic keywords:",
            search_terms['main_topic'],
            default=search_terms['main_topic'],
            key="main_select"
        )

        st.subheader("Academic Keywords (OpenAlex)")
        selected_openalex = st.multiselect(
            "Select academic keywords:",
            search_terms['openalex'],
            default=search_terms['openalex'],
            key="openalex_select"
        )

        st.subheader("Patent Keywords (PatentView)")
        selected_patentview = st.multiselect(
            "Select patent keywords:",
            search_terms['patentview'],
            default=search_terms['patentview'],
            key="patentview_select"
        )

        st.subheader("Add Manual Keywords (comma-separated)")
        additional_main = st.text_input("Add Main Topic keywords:", key="add_main")
        additional_openalex = st.text_input("Add Academic keywords:", key="add_openalex")
        additional_patentview = st.text_input("Add Patent keywords:", key="add_patentview")

        if st.button("Finalize Keywords"):

            manual_main = [kw.strip() for kw in additional_main.split(",")] if additional_main else []
            manual_openalex = [kw.strip() for kw in additional_openalex.split(",")] if additional_openalex else []
            manual_patentview = [kw.strip() for kw in additional_patentview.split(",")] if additional_patentview else []

            final_main = selected_main + manual_main
            final_openalex = selected_openalex + manual_openalex
            final_patentview = selected_patentview + manual_patentview

            st.session_state.final_keywords = {
                'main_topic': final_main,
                'openalex': final_openalex,
                'patentview': final_patentview
            }

            st.success("Keywords finalized!")
