import streamlit as st

st.set_page_config(page_title="TALK ENTREPRISE", page_icon="💬", layout="centered")

# CSS pour police et bouton en bas à gauche
st.markdown("""
<style>
body, html, [class*="css"] {
    font-family: 'Avenir Next', Arial, sans-serif !important;
}
.effacer-btn {
    border: none;
    border-radius: 9px;
    background: #f3f3f7;
    color: #7b61ff;
    font-size: 0.97em;
    font-family: 'Avenir Next', Arial, sans-serif !important;
    font-weight: 200 !important;
    letter-spacing: 0.07em;
    text-transform: lowercase;
    padding: 7px 16px;
    margin-top: 11px;
    margin-bottom: 0;
    margin-left: 0;
    cursor: pointer;
    box-shadow: none;
    transition: background 0.13s;
    text-align: left;
    display: inline-block;
}
.effacer-btn:hover {
    background: #ede7fa;
}
.chat-history {
    background: #fff;
    border-radius: 14px;
    border: 1px solid #f0f0f0;
    min-height: 170px;
    max-height: 340px;
    overflow-y: auto;
    padding: 16px 10px 10px 10px;
    margin-bottom: 2px;
    font-family: 'Avenir Next', Arial, sans-serif !important;
}
.stTextInput > div > div > input {
    border-radius: 11px !important;
    border: 1.1px solid #e3e3e3 !important;
    background: #fff !important;
    font-family: 'Avenir Next', Arial, sans-serif !important;
    font-weight: 200 !important;
    font-size: 1.04em;
    padding: 9px 12px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div style="font-family:Avenir Next, Arial, sans-serif; font-size:2.1rem; letter-spacing:0.23em; font-weight:200; text-align:center; margin-bottom:0.7em; margin-top:0.7em;">TALK ENTREPRISE</div>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage historique dans un cadre blanc discret
st.markdown('<div class="chat-history">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    who = "vous" if msg["role"] == "user" else "assistant"
    st.markdown(
        f'<span style="font-size:0.93em; color:#7b61ff; font-weight:200; letter-spacing:0.13em;">{who}</span> : '
        f'<span style="font-size:1.04em; color:#222; font-weight:200;">{msg["content"]}</span>',
        unsafe_allow_html=True
    )
st.markdown('</div>', unsafe_allow_html=True)

# Input sans placeholder
user_input = st.text_input("", key="input_text", label_visibility="collapsed")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.input_text = ""

# Ligne du bas : bouton effacer à gauche
col1, col2 = st.columns([1, 9])
with col1:
    if st.button("effacer historique", key="clear_btn", help="Supprimer tous les messages", use_container_width=False):
        st.session_state.messages = []
with col2:
    st.markdown("", unsafe_allow_html=True)
