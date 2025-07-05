import streamlit as st
import requests

st.set_page_config(page_title="Chatbot Minimaliste", page_icon="💬", layout="centered")

# Inject custom CSS for AvenirNext Ultra Light (if not available, fallback to sans-serif)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Avenir+Next:wght@200&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Avenir Next', 'AvenirNext', 'AvenirNextLTPro-UltLt', 'AvenirNext-UltraLight', 'Avenir', Arial, sans-serif !important;
        font-weight: 200 !important;
        background: #fff;
        color: #111;
        box-shadow: 0 4px 14px rgba(0,0,0,0.03);
    }
    .stTextInput > div > div > input {
        font-family: 'Avenir Next', 'AvenirNext', Arial, sans-serif !important;
        font-weight: 200 !important;
        font-size: 1.2rem;
        letter-spacing: 0.01em;
    }
    .stButton > button {
        font-family: 'Avenir Next', 'AvenirNext', Arial, sans-serif !important;
        font-weight: 200 !important;
        font-size: 1.1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    .stChatMessage {
        background: #fafbfc;
        border-radius: 18px;
        padding: 12px 16px;
        margin: 8px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    </style>
""", unsafe_allow_html=True)

st.title("💬 Chatbot Minimaliste")

# Conversation state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat input
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Envoyez un message :", "", key="input")
    submit = st.form_submit_button("Envoyer")

# Display messages
for m in st.session_state.messages:
    st.markdown(f'<div class="stChatMessage"><b>{m["role"]}:</b> {m["content"]}</div>', unsafe_allow_html=True)

# Send message to webhook and get response
if submit and user_input.strip():
    st.session_state.messages.append({"role": "Vous", "content": user_input})
    try:
        # Appelle le webhook N8n
        webhook_url = "https://leroux.app.n8n.cloud/webhook/dd642072-9735-4406-90c7-5a7a8a7ab9ea"
        response = requests.post(webhook_url, json={"message": user_input}, timeout=10)
        if response.status_code == 200:
            output = response.json().get("reply") or response.text
        else:
            output = f"Erreur Webhook ({response.status_code})"
    except Exception as e:
        output = f"Erreur de connexion : {e}"
    st.session_state.messages.append({"role": "Bot", "content": output})
    st.experimental_rerun()
