import streamlit as st
import requests

st.set_page_config(page_title="TALK ENTERPRISE", page_icon="💬", layout="centered")

# Inject custom CSS for Avenir Next, titres en majuscules, espacement lettres, bouton stylé
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@200&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Avenir Next', 'AvenirNext', 'Montserrat', Arial, sans-serif !important;
        background: #fff;
        color: #111;
        font-weight: 200 !important;
        letter-spacing: 0.01em;
    }
    .talk-title {
        font-size: 2.1rem;
        font-family: 'Avenir Next', 'AvenirNext', 'Montserrat', Arial, sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 0.25em;
        font-weight: 200 !important;
        text-align: center;
        margin-bottom: 1.2em;
        margin-top: 0.6em;
        user-select: none;
    }
    .stTextInput > div > div > input {
        font-family: 'Avenir Next', 'AvenirNext', 'Montserrat', Arial, sans-serif !important;
        font-weight: 200 !important;
        font-size: 1.16rem;
        letter-spacing: 0.08em;
        border-radius: 30px 0 0 30px !important;
        border: none !important;
        background: #f6f6f8;
        padding-left: 20px !important;
        padding-right: 38px !important;
        outline: none !important;
        box-shadow: none !important;
    }
    div[data-testid="stForm"] {
        flex-direction: row !important;
        display: flex !important;
        align-items: center;
        gap: 0 !important;
        padding-bottom: 0;
    }
    .send-btn button {
        border: none !important;
        border-radius: 50% !important;
        background: #f6f6f8 !important;
        color: #222 !important;
        font-size: 1.38rem !important;
        width: 38px !important;
        height: 38px !important;
        margin-left: -45px !important;
        margin-top: 1px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        display: flex !important;
        align-items: center;
        justify-content: center;
        transition: background 0.2s;
        cursor: pointer;
    }
    .send-btn button:hover {
        background: #e9e9ef !important;
    }
    .stChatMessage {
        background: #fafbfc;
        border-radius: 18px;
        padding: 12px 16px;
        margin: 8px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        font-family: 'Avenir Next', 'AvenirNext', 'Montserrat', Arial, sans-serif !important;
        font-weight: 200 !important;
        letter-spacing: 0.03em;
    }
    .user-msg {
        background: #e6f0fa;
        margin-left: 35%;
    }
    .bot-msg {
        background: #fafbfc;
        margin-right: 35%;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="talk-title">T A L K &nbsp; E N T E R P R I S E</div>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage de l'historique (du plus ancien au plus récent)
for m in st.session_state.messages:
    is_user = (m["role"] == "Vous")
    role_label = "VOUS" if is_user else "BOT"
    msg_class = "user-msg" if is_user else "bot-msg"
    st.markdown(
        f'<div class="stChatMessage {msg_class}"><b style="font-size:0.82em;letter-spacing:0.17em;">{role_label}</b><br>{m["content"]}</div>',
        unsafe_allow_html=True
    )

# Formulaire en ligne (input + bouton rond)
with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([15, 1])
    with col1:
        user_input = st.text_input(
            "",
            placeholder="T A P E Z &nbsp; V O T R E &nbsp; M E S S A G E...",
            key="input"
        )
    with col2:
        submit = st.form_submit_button(
            "",
            help="Envoyer",
            type="primary"
        )
        # Custom icon in button (paper plane unicode)
        st.markdown(
            """
            <style>
            [data-testid="stFormSubmitButton"] button:after {
                content: '\\1F4E7';
                font-size: 1.3em;
                position: relative;
                left: -2px;
                top: 2px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

# Gestion de l'envoi (pas de rerun)
if submit and user_input.strip():
    st.session_state.messages.append({"role": "Vous", "content": user_input})
    try:
        webhook_url = "https://leroux.app.n8n.cloud/webhook/dd642072-9735-4406-90c7-5a7a8a7ab9ea"
        response = requests.post(webhook_url, json={"query": user_input}, timeout=10)
        if response.status_code == 200:
            # On accepte "reply" ou texte brut
            try:
                data = response.json()
                output = data.get("reply") or data.get("response") or str(data)
            except Exception:
                output = response.text
        else:
            output = f"Erreur Webhook ({response.status_code})"
    except Exception as e:
        output = f"Erreur de connexion : {e}"
    st.session_state.messages.append({"role": "Bot", "content": output})
