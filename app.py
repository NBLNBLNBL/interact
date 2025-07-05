import streamlit as st
import requests

st.set_page_config(
    page_title="TALK ENTERPRISE", 
    page_icon="💬", 
    layout="centered"
)

# --- CSS pour le style et la disposition ---
st.markdown("""
    <style>
    /* Enlève la marge du container principal */
    .main .block-container {
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
        max-width: 520px;
    }
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
        margin-bottom: 1em;
        margin-top: 0.6em;
    }
    .chat-outer-box {
        background: #f5f5fb;
        border-radius: 16px;
        box-shadow: 0 2px 10px rgba(124,97,255,0.08);
        border: 1.2px solid #e9eaf3;
        margin-bottom: 0.5em;
        margin-top: 0.3em;
        min-height: 320px;
        max-height: 320px;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        overflow: hidden;
    }
    .chat-scrollbox {
        flex: 1 1 auto;
        overflow-y: auto;
        padding: 18px 8px 10px 8px;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        scroll-behavior: smooth;
    }
    .stTextInput > div > div > input {
        border-radius: 12px !important;
        border: 1.2px solid #dbeafe !important;
        background: #fff !important;
        font-size: 1.05em;
        padding: 8px 10px !important;
        margin-bottom: 0.08em;
    }
    .chat-row {
        display: flex;
        margin-bottom: 6px;
        width: 100%;
    }
    .bubble {
        max-width: 68%;
        border-radius: 17px;
        padding: 11px 16px 9px 14px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        font-family: 'Avenir Next', Arial, sans-serif !important;
        font-weight: 200 !important;
        font-size: 1.04em;
        letter-spacing: 0.02em;
        min-width: 36px;
        word-break: break-word;
        display: inline-block;
        line-height: 1.36;
    }
    .bubble-user {
        background: linear-gradient(135deg, #e6f0fa 0%, #e0e7ff 100%);
        align-self: flex-end;
        margin-left: auto;
        margin-right: 2px;
        text-align: right;
    }
    .bubble-jessica {
        background: linear-gradient(135deg, #f5edfa 0%, #f2e4ff 100%);
        align-self: flex-start;
        margin-left: 2px;
        margin-right: auto;
        text-align: left;
    }
    .bubble-label {
        font-size: 0.79em;
        text-transform: uppercase;
        letter-spacing: 0.16em;
        font-weight: 400;
        margin-bottom: 2px;
        margin-top: 0.5px;
        opacity: 0.62;
    }
    .bottom-bar {
        display: flex;
        align-items: center;
        gap: 0.4em;
        margin-top: 0.3em;
    }
    .reset-btn {
        border: none;
        border-radius: 10px;
        background: linear-gradient(135deg, #7b61ff 0%, #2684FF 100%);
        color: #fff;
        font-size: 0.98em;
        font-family: 'Avenir Next', Arial, sans-serif !important;
        letter-spacing: 0.12em;
        font-weight: 400 !important;
        text-transform: uppercase;
        padding: 7px 18px 7px 18px;
        margin-left: 0.15em;
        cursor: pointer;
        transition: background 0.18s;
        margin-bottom: 0.4em;
        margin-top: 0.2em;
    }
    .reset-btn:hover {
        background: linear-gradient(135deg, #5e45c8 0%, #1668c1 100%);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="talk-title">T A L K &nbsp; E N T E R P R I S E</div>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Chat box encadrée et scrollable ---
st.markdown('<div class="chat-outer-box"><div class="chat-scrollbox" id="chatbox">', unsafe_allow_html=True)
for m in st.session_state.messages:
    is_user = (m["role"] == "Vous")
    msg_class = "bubble-user" if is_user else "bubble-jessica"
    label = "VOUS" if is_user else "JESSICA"
    align_class = "chat-row"  # On peut jouer sur le flex si besoin
    st.markdown(
        f'<div class="{align_class}"><div style="display:flex;flex-direction:column;align-items:{"flex-end" if is_user else "flex-start"};width:100%;">'
        f'<div class="bubble-label">{label}</div>'
        f'<div class="bubble {msg_class}">{m["content"]}</div>'
        f'</div></div>',
        unsafe_allow_html=True
    )
st.markdown('</div></div>', unsafe_allow_html=True)

# --- BARRE BASSE FIXE : Champ texte et bouton reset ---
st.markdown('<div class="bottom-bar">', unsafe_allow_html=True)

def send_message():
    user_input = st.session_state.input_text.strip()
    if user_input:
        st.session_state.messages.append({"role": "Vous", "content": user_input})
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

# Champ texte
st.text_input(
    "TAPEZ VOTRE MESSAGE",
    value="",
    key="input_text",
    label_visibility="collapsed",
    on_change=send_message,
    placeholder="Taper votre message puis Entrée..."
)
# Bouton reset de l'historique collé au champ texte
reset_html = """
    <form action="" method="post">
        <button class="reset-btn" type="submit" name="reset">Effacer</button>
    </form>
"""
st.markdown(reset_html, unsafe_allow_html=True)
if st.session_state.get('reset', False):
    st.session_state.messages = []

st.markdown('</div>', unsafe_allow_html=True)

# --- Scroll auto JS (focus sur le dernier message) ---
st.markdown("""
    <script>
    setTimeout(function() {
        var chatbox = window.parent.document.getElementById("chatbox");
        if(chatbox){ chatbox.scrollTop = chatbox.scrollHeight; }
    }, 120);
    </script>
""", unsafe_allow_html=True)
