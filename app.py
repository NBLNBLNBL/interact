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
    .send-btn {
        border: none;
        border-radius: 50%;
        background: linear-gradient(135deg, #7b61ff 0%, #2684FF 100%);
        color: #fff;
        width: 44px;
        height: 44px;
        margin-left: 0.5em;
        margin-bottom: 0.18em;
        box-shadow: 0 2px 18px rgba(124,97,255,0.13);
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Avenir Next', Arial, sans-serif !important;
        font-size: 1.03rem !important;
        letter-spacing: 0.16em;
        font-weight: 200 !important;
        text-transform: uppercase;
        cursor: pointer;
        transition: background 0.15s;
    }
    .send-btn:hover {
        background: linear-gradient(135deg, #5e45c8 0%, #1668c1 100%);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="talk-title">T A L K &nbsp; E N T E R P R I S E</div>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage historique
for m in st.session_state.messages:
    is_user = (m["role"] == "Vous")
    role_label = "VOUS" if is_user else "JESSICA"
    msg_class = "user-msg" if is_user else "jessica-msg"
    st.markdown(
        f'<div class="stChatMessage {msg_class}"><b style="font-size:0.82em;letter-spacing:0.17em;">{role_label}</b><br>{m["content"]}</div>',
        unsafe_allow_html=True
    )

# Label
st.markdown('<span class="talk-label">TAPEZ VOTRE MESSAGE</span>', unsafe_allow_html=True)

# Formulaire d'envoi
with st.form(key="chat_form", clear_on_submit=True):
    c1, c2 = st.columns([17, 2])
    with c1:
        user_input = st.text_input("", value="", key="input_text", label_visibility="collapsed")
    with c2:
        send = st.form_submit_button("SEND", use_container_width=True)
    
    if send and user_input.strip():
        # Ajout message utilisateur
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
