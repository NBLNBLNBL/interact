import streamlit as st
import requests

st.set_page_config(page_title="TALK ENTREPRISE", page_icon="💬", layout="centered")

# --- CSS harmonieux pour le fond, bulles, input, etc. ---
st.markdown("""
<style>
body, html, [class*="css"] {
    font-family: 'Avenir Next', Arial, sans-serif !important;
    background: #faf8fb;
    color: #111;
}
.talk-title {
    font-size: 2.1rem;
    font-family: 'Avenir Next', Arial, sans-serif !important;
    text-transform: uppercase;
    letter-spacing: 0.24em;
    font-weight: 200 !important;
    text-align: center;
    margin-bottom: 0.6em;
    margin-top: 0.6em;
}
.chat-container {
    background: linear-gradient(120deg, #ede7fa 0%, #e4e8fa 100%);
    border-radius: 19px;
    border: 1.2px solid #e2d8fa;
    box-shadow: 0 2px 12px 0 rgba(120,80,200,.09);
    max-height: 410px;
    min-height: 220px;
    overflow-y: scroll;
    padding: 18px 6px 18px 6px;
    margin-bottom: 0.2em;
    margin-top: 0.3em;
    transition: box-shadow 0.15s;
}
.stChatMessage {
    margin-bottom: 0.09em;
}
.stTextInput > div > div > input {
    border-radius: 13px !important;
    border: 1.2px solid #c6b8e6 !important;
    background: #fff !important;
    font-family: 'Avenir Next', Arial, sans-serif !important;
    font-size: 1.03em;
    padding: 9px 12px !important;
    margin-bottom: 0.13em;
}
.st-emotion-cache-1h9usn4 {
    font-family: 'Avenir Next', Arial, sans-serif !important;
}
.stChatInputContainer {
    position: sticky !important;
    bottom: 0;
    z-index: 10;
    background: transparent !important;
    margin-top: 0.1em;
}
.reset-btn {
    border: none;
    border-radius: 11px;
    background: linear-gradient(135deg, #bfa5ff 0%, #82b5ff 100%);
    color: #2d2d52;
    font-size: 1.02em;
    font-family: 'Avenir Next', Arial, sans-serif !important;
    letter-spacing: 0.08em;
    font-weight: 500;
    text-transform: uppercase;
    padding: 8px 20px 8px 20px;
    margin-left: 0.7em;
    margin-bottom: 0.1em;
    cursor: pointer;
    box-shadow: 0 2px 8px rgba(124,97,255,0.10);
    transition: background 0.18s;
}
.reset-btn:hover {
    background: linear-gradient(135deg, #9b85cf 0%, #6497d3 100%);
    color: #fff;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="talk-title">TALK ENTREPRISE</div>', unsafe_allow_html=True)

# --- Initialisation historique ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Effacer historique ---
reset = st.button("Effacer l'historique", key="reset", help="Supprime tous les messages", use_container_width=True)
if reset:
    st.session_state.messages = []

# --- Conteneur scrollable pour les messages (avec ancre pour auto-scroll) ---
st.markdown('<div class="chat-container" id="scroller">', unsafe_allow_html=True)
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["content"])
st.markdown('<div id="anchor"></div></div>', unsafe_allow_html=True)

# --- Input sticky en bas de page ---
prompt = st.chat_input("Tapez votre message puis Entrée", key="input_text")
if prompt:
    # Ajout message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})

    # --- Appel assistant (webhook) ---
    webhook_url = "https://leroux.app.n8n.cloud/webhook/dd642072-9735-4406-90c7-5a7a8a7ab9ea"
    try:
        resp = requests.post(webhook_url, json={"query": prompt}, timeout=10)
        try:
            data = resp.json()
            reply = data.get("reply") or data.get("response") or resp.text
        except Exception:
            reply = resp.text
    except Exception:
        reply = "Jessica n'a pas pu recevoir votre message."
    # Ajout réponse assistant
    st.session_state.messages.append({"role": "assistant", "content": reply})

    # --- Auto-scroll JS ---
    st.markdown("""
        <script>
        setTimeout(function() {
            var scroller = window.parent.document.getElementById('scroller');
            var anchor = window.parent.document.getElementById('anchor');
            if (scroller && anchor) {
                anchor.scrollIntoView({ behavior: "smooth", block: "end" });
            }
        }, 80);
        </script>
    """, unsafe_allow_html=True)
