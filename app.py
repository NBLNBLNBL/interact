import streamlit as st
import requests
import time

st.set_page_config(page_title="TALK ENTERPRISE", page_icon="💬", layout="centered")

# Styles
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'Avenir Next', Arial, sans-serif !important;
        background: #fff;
        color: #111;
        font-weight: 200 !important;
        letter-spacing: 0.01em;
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
        user-select: none;
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
        user-select: none;
    }
    .talk-input {
        font-family: 'Avenir Next', Arial, sans-serif !important;
        font-weight: 200 !important;
        font-size: 1.13rem;
        letter-spacing: 0.07em;
        border-radius: 24px;
        border: none;
        background: #f6f6f8;
        padding: 14px 18px 14px 18px;
        outline: none;
        box-shadow: 0 2px 12px rgba(38,132,255,0.07);
        margin-bottom: 2px;
        width: 100%;
        transition: box-shadow 0.2s;
    }
    .talk-input:focus {
        box-shadow: 0 4px 20px rgba(38,132,255,0.13);
        background: #fafdff;
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
    .check-bar {
        display: flex; 
        flex-direction: row;
        gap: 2em;
        justify-content: flex-start;
        align-items: center;
        margin-top: 6px;
        margin-bottom: 0.7em;
        margin-left: 2px;
        font-size: 0.98em;
    }
    .check-label {
        font-size: 0.98em;
        color: #555;
        font-family: 'Avenir Next', Arial, sans-serif !important;
        letter-spacing: 0.13em;
        font-weight: 200 !important;
        user-select: none;
        margin-left: 0.45em;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="talk-title">T A L K &nbsp; E N T E R P R I S E</div>', unsafe_allow_html=True)

# State init
if "auto_send" not in st.session_state:
    st.session_state.auto_send = False
if "enter_send" not in st.session_state:
    st.session_state.enter_send = True
if "messages" not in st.session_state:
    st.session_state.messages = []
if "input" not in st.session_state:
    st.session_state.input = ""
if "last_edit_time" not in st.session_state:
    st.session_state.last_edit_time = 0.0
if "pending_send" not in st.session_state:
    st.session_state.pending_send = False

# Affichage historique
for m in st.session_state.messages:
    is_user = (m["role"] == "Vous")
    role_label = "VOUS" if is_user else "JESSICA"
    msg_class = "user-msg" if is_user else "jessica-msg"
    st.markdown(
        f'<div class="stChatMessage {msg_class}"><b style="font-size:0.82em;letter-spacing:0.17em;">{role_label}</b><br>{m["content"]}</div>',
        unsafe_allow_html=True
    )

# Label au-dessus du champ
st.markdown('<span class="talk-label">TAPEZ VOTRE MESSAGE</span>', unsafe_allow_html=True)

# Switches
col1, col2 = st.columns([1, 1])
with col1:
    auto_send = st.checkbox(
        "Auto-send",
        value=st.session_state.auto_send,
        key="auto-send",
        help="Envoie auto après 3s d'inactivité."
    )
with col2:
    enter_send = st.checkbox(
        "Enter-send",
        value=st.session_state.enter_send,
        key="enter-send",
        help="Envoi du message avec entrée."
    )
st.session_state.auto_send = auto_send
st.session_state.enter_send = enter_send

# Barre de saisie + bouton SEND si enter_send désactivé
c1, c2 = st.columns([17, 2])
with c1:
    input_text = st.text_input(
        "",
        value=st.session_state.input,
        key="talk_input",
        label_visibility="collapsed"
    )
with c2:
    send_btn = False
    if not st.session_state.enter_send:
        send_btn = st.button("SEND", key="send-btn", help="Envoyer", type="primary")

# Détection de frappe pour autosend
now = time.time()
if input_text != st.session_state.input:
    st.session_state.input = input_text
    st.session_state.last_edit_time = now
    st.session_state.pending_send = False

def really_send(msg):
    st.session_state.messages.append({"role": "Vous", "content": msg})
    webhook_url = "https://leroux.app.n8n.cloud/webhook/dd642072-9735-4406-90c7-5a7a8a7ab9ea"
    try:
        resp = requests.post(webhook_url, json={"query": msg}, timeout=10)
        # Affiche la réponse de Jessica (ici message fixe pour le test)
        reply = "Votre message a bien été reçu."
    except Exception:
        reply = "Jessica n'a pas pu recevoir votre message."
    st.session_state.messages.append({"role": "Jessica", "content": reply})
    st.session_state.input = ""
    st.session_state.talk_input = ""
    st.session_state.pending_send = False

# Autosend
if st.session_state.auto_send and st.session_state.input.strip():
    # Si on n'a pas déjà pending_send, et que 3s sont écoulées depuis la dernière frappe
    if not st.session_state.pending_send and (now - st.session_state.last_edit_time) > 3:
        st.session_state.pending_send = True
        really_send(st.session_state.input)
        st.experimental_rerun()

# Enter-send
elif st.session_state.enter_send:
    # On détecte l'envoi via Entrée (Streamlit vide le champ après submit)
    if st.session_state.input != "" and input_text == "":
        really_send(st.session_state.input)
        st.experimental_rerun()

# SEND bouton
elif send_btn and st.session_state.input.strip():
    really_send(st.session_state.input)
    st.experimental_rerun()
