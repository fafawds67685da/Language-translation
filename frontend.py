import streamlit as st
import requests

# FastAPI backend URL
API_URL = "http://localhost:8000/translate"

# App title
st.title("Indian Language Translator")

# Language dropdown
language = st.selectbox(
    "Choose the target language:",
    ["Hindi", "Malayalam", "Marathi", "Urdu"]
)

# Language code mapping
language_map = {
    "Hindi": "hindi",
    "Malayalam": "malayalam",
    "Marathi": "marathi",
    "Urdu": "urdu"
}

# Session state for input/output text
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""
if "text_input" not in st.session_state:
    st.session_state.text_input = ""

# Input-output columns
col1, col2 = st.columns(2)

# English input
with col1:
    st.session_state.text_input = st.text_area("English Text:", value=st.session_state.text_input, height=200)

# Translated text
with col2:
    st.text_area("Translated Text:", value=st.session_state.translated_text, height=200, disabled=True)

# Translate button
if st.button("Translate"):
    if st.session_state.text_input.strip():
        try:
            response = requests.post(
                f"{API_URL}/{language_map[language]}",
                json={"text": st.session_state.text_input}
            )
            response.raise_for_status()
            data = response.json()
            st.session_state.translated_text = data["translated_text"]
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching translation: {e}")
    else:
        st.warning("Please enter some text to translate.")
