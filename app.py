import streamlit as st
import requests

st.set_page_config(page_title="TALK ENTERPRISE", page_icon="💬", layout="centered")

# --- CSS ---
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
    .history-scroll {
        max-height: 180px;
        overflow-y: auto;
        border: 1px solid #f0f0f0;
        border-radius: 12px;
        margin-bottom: 16px;
        padding: 8px 0 8px 0;
        background: #fdfdfd;
        box-shadow: none;
    }
    .stTextInput > div > div > input {
        border-radius: 12px !important;
        border: 1.2px solid #dbeafe !important;
        background: #fff !important;
        font-size: 1.05em;
        padding: 8px 10px !important;
        margin-bottom: 0.3em;
        box-shadow: none !important;
    }
    .reset-btn {
        background: transparent;
        color: #A0A0A0;
        border: none;
        font-size: 0.92em;
        margin-left: 6px;
        margin-top: 2px;
        padding: 0 8px;
        cursor: pointer;
        transition: color 0.2s;
        border-radius: 8px;
    }
    .reset-btn:hover {
        color: #7b61ff;
        background: #f3f0ff;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="talk-title">T A L K &nbsp; E N T E R P R I S E</div>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

MAX_PRIMARY = 3  # Nombre d'interactions primaires visibles "en gros"

# --- HISTORIQUE SCROLLABLE ---
st.markdown('<div class="talk-label">Historique</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="history-scroll">', unsafe_allow_html=True)
    for m in st.session_state.messages:
        is_user = (m["role"] == "Vous")
        role_label = "VOUS" if is_user else "JESSICA"
        msg_class = "user-msg" if is_user else "jessica-msg"
        st.markdown(
            f'<div class="stChatMessage {msg_class}" style="margin-left:0;margin-right:0;"><b style="font-size:0.82em;letter-spacing:0.17em;">{role_label}</b><br>{m["content"]}</div>',
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

# --- PRIMARY (3 dernières interactions) ---
st.markdown('<div class="talk-label">Derniers échanges</div>', unsafe_allow_html=True)
with st.container():
    for m in st.session_state.messages[-MAX_PRIMARY:]:
        is_user = (m["role"] == "Vous")
        role_label = "VOUS" if is_user else "JESSICA"
        msg_class = "user-msg" if is_user else "jessica-msg"
        st.markdown(
            f'<div class="stChatMessage {msg_class}"><b style="font-size:0.82em;letter-spacing:0.17em;">{role_label}</b><br>{m["content"]}</div>',
            unsafe_allow_html=True
        )

# --- INPUT ---
st.markdown('<span class="talk-label">TAPER VOTRE MESSAGE</span>', unsafe_allow_html=True)

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
        st.session_state.messages.append({"role": "Jessica", "content": reply})
        st.session_state.input_text = ""

# Champ texte sans bouton Send
st.text_input(
    "",
    value="",
    key="input_text",
    label_visibility="collapsed",
    on_change=send_message
)

# --- RESET DISCRET ---
st.markdown(
    '<button class="reset-btn" onclick="window.location.reload()">Reset</button>',
    unsafe_allow_html=True,
)
