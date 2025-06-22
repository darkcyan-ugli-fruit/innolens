# src/config/openai_config.py

import streamlit as st

OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in Streamlit secrets.")
