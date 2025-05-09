import streamlit as st
import requests

API_URL = "http://localhost:8000/translate"
AUDIO_URL = "http://localhost:8000/audio"

st.title("Indian Language Translator")

language = st.selectbox("Choose the target language:", ["Hindi", "Malayalam", "Marathi", "Urdu"])

language_map = {
    "Hindi": "hindi",
    "Malayalam": "malayalam",
    "Marathi": "marathi",
    "Urdu": "urdu"
}

if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""
if "audio_bytes" not in st.session_state:
    st.session_state.audio_bytes = None
if "text_input" not in st.session_state:
    st.session_state.text_input = ""

col1, col2 = st.columns(2)

with col1:
    st.session_state.text_input = st.text_area("English Text:", value=st.session_state.text_input, height=200)

with col2:
    st.text_area("Translated Text:", value=st.session_state.translated_text, height=200, disabled=True)

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

            # Fetch audio
            audio_response = requests.get(f"{AUDIO_URL}/{data['audio_file']}")
            if audio_response.status_code == 200:
                st.session_state.audio_bytes = audio_response.content
            else:
                st.warning("Failed to fetch audio.")

        except requests.exceptions.RequestException as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter some text to translate.")

if st.session_state.audio_bytes:
    st.audio(st.session_state.audio_bytes, format="audio/mp3")
