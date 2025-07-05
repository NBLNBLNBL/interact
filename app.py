import streamlit as st
import requests

st.set_page_config(page_title="TALK ENTERPRISE", page_icon="💬", layout="centered")

# CSS
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'Avenir Next', Arial, sans-serif !important;
        background: #fff;
        color: #111;
    }
    .talk-title {
        font-size: 2.1rem;
        font-family: 'Avenir Next', Arial, sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 0.25em;
        font-weight: 200 !important;
        text-align: center;
        margin-bottom: 1.2em;
        margin-top: 0.6em;
    }
    .talk-label {
        font-size: 0.82rem;
        color: #666;
        font-family: 'Avenir Next', Arial, sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 0.18em;
        font-weight: 200 !important;
        margin-left: 6px;
        margin-bottom: 2px;
        margin-top: 12px;
        display: block;
    }
    .stChatMessage {
        background: #fafbfc;
        border-radius: 18px;
        padding: 12px 16px;
        margin: 8px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        font-family: 'Avenir Next', Arial, sans-serif !important;
        font-weight: 200 !important;
        letter-spacing: 0.03em;
    }
    .user-msg {
        background: #e6f0fa;
        margin-left: 35%;
    }
    .jessica-msg {
        background: #f5edfa;
        margin-right: 35%;
    }
    .history-container {
        max-height: 270px;
        overflow-y: auto;
        margin-bottom: 1em;
        scroll-behavior: smooth;
        border-radius: 14px;
        border: 1px solid #eee;
        background: #fff;
        padding: 10px 0 8px 0;
        min-height: 90px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .stTextInput > div > div > input {
        border-radius: 12px !important;
        border: 1.2px solid #dbeafe !important;
        background: #fff !important;
        font-size: 1.05em;
        padding: 8px 10px !important;
        margin-bottom: 0.3em;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="talk-title">T A L K &nbsp; E N T E R P R I S E</div>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

MAX_HISTORY = 3  # Nombre de messages affichés en permanence (les plus récents)

# Affichage historique dans un conteneur scrollable, mais on montre toujours les 3 derniers messages
with st.container():
    st.markdown('<div class="history-container">', unsafe_allow_html=True)
    # On limite l'affichage aux MAX_HISTORY derniers messages mais on garde tout l'historique en mémoire
    for m in st.session_state.messages[-MAX_HISTORY:]:
        is_user = (m["role"] == "Vous")
        role_label = "VOUS" if is_user else "JESSICA"
        msg_class = "user-msg" if is_user else "jessica-msg"
        st.markdown(
            f'<div class="stChatMessage {msg_class}"><b style="font-size:0.82em;letter-spacing:0.17em;">{role_label}</b><br>{m["content"]}</div>',
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

# Label
st.markdown('<span class="talk-label">TAPEZ VOTRE MESSAGE</span>', unsafe_allow_html=True)

# Formulaire d'envoi
# Plus de bouton "Send" ! On envoie uniquement avec "Enter".
def send_message():
    user_input = st.session_state.input_text.strip()
    if user_input:
        # Ajout message utilisateur D'ABORD
        st.session_state.messages.append({"role": "Vous", "content": user_input})

        # Envoi webhook
        webhook_url = "https://leroux.app.n8n.cloud/webhook/dd642072-9735-4406-90c7-5a7a8a7ab9ea"
        try:
            resp = requests.post(webhook_url, json={"query": user_input}, timeout=10)
            try:
                data = resp.json()
                reply = data.get("reply") or data.get("response") or resp.text
            except Exception:
                reply = resp.text
        except Exception:
            reply = "Jessica n'a pas pu recevoir votre message."
        # Ajout réponse Jessica
        st.session_state.messages.append({"role": "Jessica", "content": reply})

        # Efface le champ input
        st.session_state.input_text = ""

# Champ de texte (sans bouton "Send")
user_input = st.text_input(
    "",
    value="",
    key="input_text",
    label_visibility="collapsed",
    on_change=send_message
)

# Optionnel : bouton pour effacer l'historique complet
if st.button("Effacer l'historique", help="Supprime tous les messages de la session."):
    st.session_state.messages = []

# Scroll automatique vers le bas (hack Streamlit)
st.markdown("""
    <script>
    var h = window.parent.document.querySelector('.main .block-container');
    if (h) { h.scrollTop = h.scrollHeight; }
    </script>
""", unsafe_allow_html=True)
