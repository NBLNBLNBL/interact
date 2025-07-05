import streamlit as st
import requests
import time

st.set_page_config(page_title="TALK ENTERPRISE", page_icon="💬", layout="centered")

# CSS ultra minimaliste et design
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
    .talk-label {
        font-size: 0.82rem;
        color: #666;
        font-family: 'Avenir Next', 'AvenirNext', 'Montserrat', Arial, sans-serif !important;
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
        font-family: 'Avenir Next', 'AvenirNext', 'Montserrat', Arial, sans-serif !important;
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
        font-family: 'Avenir Next', 'AvenirNext', 'Montserrat', Arial, sans-serif !important;
        letter-spacing: 0.13em;
        font-weight: 200 !important;
        user-select: none;
        margin-left: 0.45em;
    }
    .send-btn-float {
        position: fixed;
        bottom: 34px;
        right: 38px;
        z-index: 99;
    }
    .send-fab-btn {
        border: none;
        border-radius: 50%;
        background: linear-gradient(135deg, #7b61ff 0%, #2684FF 100%);
        color: #fff;
        width: 40px;
        height: 40px;
        box-shadow: 0 2px 18px rgba(124,97,255,0.19);
        display: flex;
        align-items: center;
        justify-content: center;
        transition: background 0.15s;
        cursor: pointer;
        font-size: 1.22rem;
        outline: none !important;
    }
    .send-fab-btn:hover {
        background: linear-gradient(135deg, #5e45c8 0%, #1668c1 100%);
    }
    .send-fab-btn svg {
        width: 19px;
        height: 19px;
        display: block;
        margin: auto;
        margin-top: 0;
        margin-left: 1px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="talk-title">T A L K &nbsp; E N T E R P R I S E</div>', unsafe_allow_html=True)

# Persistance des settings avec st.session_state
if "auto_send" not in st.session_state:
    st.session_state.auto_send = False
if "enter_send" not in st.session_state:
    st.session_state.enter_send = True
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_input" not in st.session_state:
    st.session_state.last_input = ""
if "input_time" not in st.session_state:
    st.session_state.input_time = 0

# JS pour persister les switches (via localStorage)
st.markdown("""
<script>
(function(){
    const keyAuto = "talk_ent_auto_send";
    const keyEnter = "talk_ent_enter_send";
    // On load, set state from localStorage (Streamlit reloads may lose state otherwise)
    window.addEventListener("DOMContentLoaded", () => {
        const autoSend = localStorage.getItem(keyAuto) === "true";
        const enterSend = localStorage.getItem(keyEnter) !== "false";
        window.parent.postMessage({type: "streamlit:setComponentValue", key: "auto_send", value: autoSend}, "*");
        window.parent.postMessage({type: "streamlit:setComponentValue", key: "enter_send", value: enterSend}, "*");
    });
    // On change, monitor inputs
    window.addEventListener("input", e => {
        if(e.target.id && e.target.id.includes("auto-send")) {
            localStorage.setItem(keyAuto, e.target.checked);
        }
        if(e.target.id && e.target.id.includes("enter-send")) {
            localStorage.setItem(keyEnter, e.target.checked);
        }
    });
})();
</script>
""", unsafe_allow_html=True)

# Affichage historique
for m in st.session_state.messages:
    is_user = (m["role"] == "Vous")
    role_label = "VOUS" if is_user else "JESSICA"
    msg_class = "user-msg" if is_user else "jessica-msg"
    st.markdown(
        f'<div class="stChatMessage {msg_class}"><b style="font-size:0.82em;letter-spacing:0.17em;">{role_label}</b><br>{m["content"]}</div>',
        unsafe_allow_html=True
    )

# Label ultra fin au-dessus du champ
st.markdown('<span class="talk-label">TAPEZ VOTRE MESSAGE</span>', unsafe_allow_html=True)

# Champ texte custom (sans placeholder)
user_input = st.text_input(
    "",
    value=st.session_state.last_input,
    key="talk_input",
    label_visibility="collapsed",
)

# Bar switches
col1, col2 = st.columns([1, 1])
with col1:
    auto_send = st.checkbox(
        "Auto-send",
        value=st.session_state.auto_send,
        key="auto-send",
        help="Envoie auto après 3s d'inactivité.",
    )
with col2:
    enter_send = st.checkbox(
        "Enter-send",
        value=st.session_state.enter_send,
        key="enter-send",
        help="Envoi du message avec entrée.",
    )

# Mémorise dans session_state & localStorage
st.session_state.auto_send = auto_send
st.session_state.enter_send = enter_send

# Timer pour auto-send
def auto_send_trigger():
    if st.session_state.auto_send and st.session_state.last_input.strip():
        now = time.time()
        if now - st.session_state.input_time > 3:
            return True
    return False

# Listen for input changes
if user_input != st.session_state.last_input:
    st.session_state.last_input = user_input
    st.session_state.input_time = time.time()

# Envoi message
def send_message():
    msg = st.session_state.last_input.strip()
    if not msg:
        return
    st.session_state.messages.append({"role": "Vous", "content": msg})
    st.session_state.last_input = ""
    webhook_url = "https://leroux.app.n8n.cloud/webhook/dd642072-9735-4406-90c7-5a7a8a7ab9ea"
    try:
        resp = requests.post(webhook_url, json={"query": msg}, timeout=10)
        if resp.status_code == 200:
            try:
                data = resp.json()
                output = data.get("reply") or data.get("response") or str(data)
            except Exception:
                output = resp.text
        else:
            output = f"Erreur Webhook ({resp.status_code})"
    except Exception as e:
        output = f"Erreur de connexion : {e}"
    st.session_state.messages.append({"role": "Jessica", "content": output})

# Enter-send: on submit
if st.session_state.enter_send:
    # Utilise le comportement natif de Streamlit (Enter pour submit)
    form = st.form("form_enter_send", clear_on_submit=True)
    with form:
        form_input = st.text_input(
            "",
            value=st.session_state.last_input,
            key="talk_input_form",
            label_visibility="collapsed"
        )
        submitted = st.form_submit_button("SEND")
    if submitted and form_input.strip():
        st.session_state.last_input = form_input
        send_message()
        st.experimental_rerun()
    elif auto_send_trigger():
        send_message()
        st.experimental_rerun()
else:
    # Affiche le bouton d'envoi violet, bas droite
    if auto_send_trigger():
        send_message()
        st.experimental_rerun()
    st.markdown("""
    <div class="send-btn-float">
        <form action="#" method="post">
            <button class="send-fab-btn" name="sendbtn" type="submit" title="Envoyer">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M12 4L12 20M12 4L6 10M12 4L18 10" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </button>
        </form>
    </div>
    """, unsafe_allow_html=True)
    if st.session_state.get("sendbtn") or st.session_state.get("sendbtn_clicked"):
        send_message()
        st.experimental_rerun()
