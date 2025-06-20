# src/app/ui/keyword_display.py

import streamlit as st

def display_final_keywords():
    if st.session_state.final_keywords:
        st.header("Step 3 — Display Final Keywords")
        st.write("### Final Selected Keywords")
        st.write("Main Topic:", st.session_state.final_keywords['main_topic'])
        st.write("Secondary Topic:", st.session_state.final_keywords['secondary_topic'])
        # st.write("PatentView Keywords:", st.session_state.final_keywords['patentview'])

        # st.markdown("""
        # ### 🔄 Next Steps Pipeline (TO BE BUILT):

        # 1️⃣ **OpenAlex API** — Use finalized keywords to query publications  
        # 2️⃣ **PatentView API** — Use finalized keywords to query patents  
        # 3️⃣ **FDA Device Matching** — Match organizations vs approved devices  
        # 4️⃣ **Data Cleaning & Normalization** — Apply name normalization  
        # 5️⃣ **Company Classification** — Use OpenAI classification model  
        # 6️⃣ **Insight Generation** — Generate final scouting report
        # """)

        # if st.button("Load Data (future step placeholder)"):
        #     st.write("⚠ Here you'll call PatentView, OpenAlex and FDA APIs.")
