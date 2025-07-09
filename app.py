import streamlit as st
import requests
from audio_scraper_module import scrape_files

st.set_page_config(page_title="TALKENTREPRISE", page_icon="💬", layout="centered")

# CSS Avenir Next minimaliste
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
.stButton>button {
    border-radius: 9px !important;
    border: 1px solid #e3e3e3 !important;
    background: #fff !important;
    color: #000 !important;
    font-family: 'Avenir Next', Arial, sans-serif !important;
    font-weight: 200 !important;
    letter-spacing: 0.13em;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="titre">TALKENTREPRISE</div>', unsafe_allow_html=True)

# Fonction appelée à chaque "Entrée"
def send_and_clear():
    user_input = st.session_state.input_text
    if user_input.strip():
        webhook_url = "https://leroux.app.n8n.cloud/webhook/dd642072-9735-4406-90c7-5a7a8a7ab9ea"
        try:
            requests.post(webhook_url, json={"query": user_input}, timeout=10)
        except Exception:
            pass
    st.session_state.input_text = ""

st.text_input("", key="input_text", label_visibility="collapsed", on_change=send_and_clear)

# Etat pour l'interface de scraping
if 'scraper_active' not in st.session_state:
    st.session_state.scraper_active = False

if st.button("ACTIVER WEB AUDIO SCRAPING"):
    st.session_state.scraper_active = not st.session_state.scraper_active

if st.session_state.scraper_active:
    st.markdown("<div class='titre'>WEB SCRAPER</div>", unsafe_allow_html=True)
    with st.form("scraper_form"):
        site_url = st.text_input("URL DU SITE", placeholder="https://example.com")
        mode = st.radio("FICHIERS À EXTRAIRE", ["Audios", "PDF"], horizontal=True)
        submitted = st.form_submit_button("LANCER")
        if submitted and site_url:
            mode_key = "audio" if mode == "Audios" else "pdf"
            links = scrape_files(site_url, mode=mode_key)
            if links:
                st.write("Trouvés :")
                for l in links:
                    st.write(l)
            else:
                st.write("Aucun fichier trouvé.")
