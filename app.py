import streamlit as st
import requests

st.set_page_config(
    page_title="TALK ENTERPRISE", 
    page_icon="💬",
    layout="centered"
)

# --- CSS ---
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Avenir Next', Arial, sans-serif !important;
        background: #f5f6fa !important;
        color: #111;
    }
    .talk-title {
        font-size: 2.1rem;
        font-family: 'Avenir Next', Arial, sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 0.25em;
        font-weight: 200 !important;
        text-align: center;
        margin-bottom: 0.7em;
        margin-top: 0.6em;
    }
    .chat-history {
        max-height: 350px;
        overflow-y: auto;
        background: #fff;
        border-radius: 18px;
        box-shadow: 0 2px 12px 0 rgba(120, 120, 130, 0.10);
        padding: 18px 10px 18px 10px;
        margin-bottom: 18px;
        border: 1.3px solid #ececec;
    }
    .bubble {
        display: flex;
        flex-direction: column;
        max-width: 67%;
        margin-bottom: 8px;
        font-family: 'Avenir Next', Arial, sans-serif !important;
        font-size: 1.05em;
        word-break: break-word;
    }
    .bubble.user {
        align-self: flex-end;
        background: linear-gradient(135deg, #e5f0fd 0%, #d1e3ff 100%);
        color: #222;
        border-radius: 20px 20px 8px 20px;
        box-shadow: 0 1px 4px 0 rgba(100,140,255,0.08);
        padding: 9px 15px 9px 15px;
        margin-right: 4px;
    }
    .bubble.jessica {
        align-self: flex-start;
        background: linear-gradient(135deg, #f7eefc 0%, #f4f5fa 100%);
        color: #333;
        border-radius: 20px 20px 20px 8px;
        box-shadow: 0 1px 4px 0 rgba(170,130,255,0.08);
        padding: 9px 15px 9px 15px;
        margin-left: 4px;
    }
    .bubble-label {
        font-size: 0.78em;
        color: #888a;
        margin-bottom: 2px;
        letter-spacing: 0.10em;
        text-align: left;
    }
    .bubble.user .bubble-label {
        text-align: right;
        color: #6d7bbd;
    }
    .bubble.jessica .bubble-label {
        color: #ae8fc7;
    }
    .input-area {
        background: #fff;
        border-radius: 16px;
        box-shadow: 0 1px 6px 0 rgba(120, 120, 130, 0.13);
        padding: 10px 14px;
        margin-bottom: 5px;
        border: 1.2px solid #dbeafe;
        display: flex;
        align-items: center;
    }
    .stTextInput > div > div > input {
        background: transparent !important;
        border: none !important;
        padding: 6px 4px !important;
        font-size: 1.07em;
        color: #333 !important;
        margin-bottom: 0 !important;
        box-shadow: none !important;
        outline: none !important;
    }
    .reset-btn {
        background: transparent;
        color: #a5a5b6;
        border: none;
        font-size: 1em;
        margin-left: 0.4em;
        margin-top: 0.13em;
        padding: 4px 11px;
        cursor: pointer;
        border-radius: 8px;
        transition: background 0.18s, color 0.18s;
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

# --- BOUTON RESET ---
def reset_chat():
    st.session_state.messages = []

st.markdown(
    '<button class="reset-btn" onclick="window.dispatchEvent(new CustomEvent(\'reset_chat\'));">Reset</button>',
    unsafe_allow_html=True,
)
st.session_state['do_reset'] = st.session_state.get('do_reset', False)
if st.session_state['do_reset']:
    reset_chat()
    st.session_state['do_reset'] = False

# Petite astuce JS pour le bouton reset (Streamlit ne supporte pas nativement le onclick qui touche Python)
st.markdown("""
    <script>
    window.addEventListener('reset_chat', function() {
        window.parent.postMessage({isStreamlitMessage: true, type: 'streamlit:setComponentValue', value: true, key: 'do_reset'}, '*');
    });
    </script>
""", unsafe_allow_html=True)

# --- AFFICHAGE DU CHAT AVEC SCROLL ---
st.markdown('<div class="chat-history">', unsafe_allow_html=True)
for m in st.session_state.messages:
    role = m["role"]
    content = m["content"]
    if role.lower() == "vous":
        bubble_class = "bubble user"
        label = "VOUS"
    else:
        bubble_class = "bubble jessica"
        label = "JESSICA"
    st.markdown(
        f'<div class="{bubble_class}"><div class="bubble-label">{label}</div>{content}</div>',
        unsafe_allow_html=True
    )
st.markdown('</div>', unsafe_allow_html=True)

# --- INPUT AREA ---
def send_message():
    user_input = st.session_state.input_text.strip()
    if user_input:
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

st.markdown('<div class="input-area">', unsafe_allow_html=True)
st.text_input(
    "",
    value="",
    key="input_text",
    label_visibility="collapsed",
    on_change=send_message
)
st.markdown('</div>', unsafe_allow_html=True)
