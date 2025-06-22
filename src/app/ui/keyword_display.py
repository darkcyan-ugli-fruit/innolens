# src/app/ui/keyword_display.py

import streamlit as st

def display_final_keywords():
    if st.session_state.final_keywords:
        st.header("Step 3 — Display Final Keywords")
        st.write("### Final Selected Keywords")
        st.write("Main Topic:", st.session_state.final_keywords['main_topic'])
        st.write("Secondary Topic:", st.session_state.final_keywords['secondary_topic'])
        # st.write("PatentView Keywords:", st.session_state.final_keywords['patentview'])

    