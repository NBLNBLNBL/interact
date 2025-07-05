import streamlit as st
import requests

st.set_page_config(page_title="TALKENTREPRISE", page_icon="💬", layout="centered")

# CSS pour tout en majuscules, police Avenir Next, et bouton discret
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
.untreat-btn {
    border: none;
    border-radius: 8px;
    background: transparent;
    color: #7b61ff;
    font-size: 0.97em;
    font-family: 'Avenir Next', Arial, sans-serif !important;
    font-weight: 500;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    padding: 6px 16px 6px 10px;
    margin-left: 0;
    margin-top: 7px;
    margin-bottom: 0;
    cursor: pointer;
    transition: background 0.13s, color 0.13s;
    display: inline-block;
    box-shadow: none;
    outline: none;
}
.untreat-btn:hover {
    background: #f4f4fa;
    color: #5e45c8;
}
</style>
""", unsafe_allow_html=True)

# Titre principal en majuscules
st.markdown('<div class="titre">TALKENTREPRISE</div>', unsafe_allow_html=True)

# Barre de texte et bouton "UNTREAT"
col1, col2 = st.columns([8, 2])
with col1:
    user_input = st.text_input("", key="input_text", label_visibility="collapsed")
with col2:
    send = st.button("UNTREAT", key="untreat_btn", use_container_width=True)

# Envoi au webhook et reset du champ
if send and user_input.strip():
    webhook_url = "https://leroux.app.n8n.cloud/webhook/dd642072-9735-4406-90c7-5a7a8a7ab9ea"
    try:
        requests.post(webhook_url, json={"query": user_input}, timeout=10)
    except Exception:
        pass
    st.session_state.input_text = ""
