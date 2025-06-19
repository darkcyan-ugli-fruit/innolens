import streamlit as st

def run_keyword_review():
    if "search_terms" in st.session_state and st.session_state.search_terms:
        st.header("Step 2 — Review Keywords & Manual Editing")

        search_terms = st.session_state["search_terms"]
        main_topic = search_terms.get("main_topic", [])
        secondary_topic = search_terms.get("secondary_topic", [])

        st.subheader("Main Topic")
        selected_main = st.multiselect(
            "Select main topic keywords:",
            main_topic,
            default=main_topic,
            key="main_select"
        )

        st.subheader("Secondary Topic")
        selected_secondary = st.multiselect(
            "Select academic keywords:",
            secondary_topic,
            default=secondary_topic,
            key="secondary_topic_select"
        )

        st.subheader("Add Manual Keywords (comma-separated)")
        additional_main = st.text_input("Add Main Topic keywords:", key="add_main")
        additional_secondary = st.text_input("Add Secondary keywords:", key="add_secondary")

        if st.button("Finalize Keywords"):
            manual_main = [kw.strip() for kw in additional_main.split(",") if kw.strip()]
            manual_secondary = [kw.strip() for kw in additional_secondary.split(",") if kw.strip()]

            final_keywords = {
                "main_topic": selected_main + manual_main,
                "secondary_topic": selected_secondary + manual_secondary
            }

            st.session_state.final_keywords = final_keywords
            st.success("Keywords finalized!")
