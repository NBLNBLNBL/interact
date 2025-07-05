import streamlit as st

st.set_page_config(page_title="TalkEntreprise", page_icon="💬", layout="centered")

# CSS minimaliste pour tout uniformiser
st.markdown("""
<style>
body, html, [class*="css"] {
    font-family: 'Avenir Next', Arial, sans-serif !important;
}
.titre {
    font-family: 'Avenir Next', Arial, sans-serif !important;
    font-size: 2.1rem;
    letter-spacing: 0.23em;
    font-weight: 200;
    text-align: center;
    margin-bottom: 1.2em;
    margin-top: 0.9em;
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
.reset-btn {
    border: none;
    border-radius: 8px;
    background: transparent;
    color: #8c8caa;
    font-size: 0.85em;
    font-family: 'Avenir Next', Arial, sans-serif !important;
    font-weight: 200;
    letter-spacing: 0.09em;
    text-transform: lowercase;
    padding: 4px 14px 4px 8px;
    margin-left: 0;
    margin-top: 7px;
    margin-bottom: 0;
    cursor: pointer;
    transition: background 0.13s, color 0.13s;
    display: inline-block;
    box-shadow: none;
    outline: none;
}
.reset-btn:hover {
    background: #f4f4fa;
    color: #7b61ff;
}
</style>
""", unsafe_allow_html=True)

# Titre
st.markdown('<div class="titre">TalkEntreprise</div>', unsafe_allow_html=True)

# Zone texte (aucun placeholder)
st.text_input("", key="input_text", label_visibility="collapsed")

# Ligne du bas : bouton reset à gauche, petit et discret
col1, col2 = st.columns([1, 9])
with col1:
    st.markdown(
        '''<form action="" method="post" style="margin:0;">
        <button class="reset-btn" type="submit" name="reset">reset</button>
        </form>''',
        unsafe_allow_html=True
    )
with col2:
    st.markdown("", unsafe_allow_html=True)
