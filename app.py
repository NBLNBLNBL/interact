import streamlit as st
import requests

st.set_page_config(page_title="TALKENTREPRISE", page_icon="💬", layout="centered")

# CSS : tout Avenir Next, tout en majuscules
st.markdown("""
<style>
body, html, [class*="css"] {
    font-family: 'Avenir Next', Arial, sans-serif !important;
}
.titre {
    font-family: 'Avenir Next', Arial, sans-serif !important;
    font-size: 2.1rem;
    letter-spacing: 0.23em;
    font-weight: 200;
    text-align: center;
    margin-bottom: 1.2em;
    margin-top: 0.9em;
    text-transform: uppercase;
}
.stTextInput > div > div > input {
    border-radius: 11px !important;
    border: 1.1px solid #e3e3e3 !important;
    background: #fff !important;
    font-family: 'Avenir Next', Arial, sans-serif !important;
    font-weight: 200 !important;
    font-size: 1.04em;
    padding: 9px 12px !important;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)

# Titre
st.markdown('<div class="titre">TALKENTREPRISE</div>', unsafe_allow_html=True)

# Zone de texte : envoi au webhook à "enter", pas de bouton
user_input = st.text_input("", key="input_text", label_visibility="collapsed")

if user_input:
    webhook_url = "https://leroux.app.n8n.cloud/webhook/dd642072-9735-4406-90c7-5a7a8a7ab9ea"
    try:
        requests.post(webhook_url, json={"query": user_input}, timeout=10)
    except Exception:
        pass
    st.session_state.input_text = ""
