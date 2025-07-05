import streamlit as st
import requests

st.set_page_config(page_title="TALKENTREPRISE", page_icon="💬", layout="centered")

st.markdown("""
<style>
body, html, [class*="css"] {
    font-family: 'Avenir Next', Arial, sans-serif !important;
    background: #f6f6fa !important;
    border-radius: 24px !important;
}
.titre {
    font-family: 'Avenir Next', Arial, sans-serif !important;
    font-size: 2.1rem;
    letter-spacing: 0.23em;
    font-weight: 200;
    text-align: center;
    margin-bottom: 1.2em;
    margin-top: 0.9em;
    text-transform: uppercase;
    border-radius: 24px !important;
}
.stTextInput > div > div > input {
    border-radius: 24px !important;
    border: 1.1px solid #e3e3e3 !important;
    background: #fff !important;
    font-family: 'Avenir Next', Arial, sans-serif !important;
    font-weight: 200 !important;
    font-size: 1.04em;
    padding: 9px 12px !important;
}
.totalresult-text {
    font-family: 'Avenir Next', Arial, sans-serif !important;
    font-size: 0.97em;
    font-weight: 200;
    color: #b6b6c2;
    letter-spacing: 0.07em;
    margin-bottom: 1.0em;
    text-align: center;
}
.results-row {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 2.1em;
    margin-bottom: 1.2em;
    border-radius: 24px !important;
}
.result-card {
    background: #f9f9fb;
    border-radius: 24px !important;
    box-shadow: 0 4px 24px 0 rgba(30,30,68,0.08), 0 1.5px 4px #ececf3;
    padding: 30px 34px 26px 34px;
    min-width: 320px;
    max-width: 380px;
    min-height: 180px;
    border: 1px solid #f2f2f6;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    word-break: break-word;
    white-space: normal;
}
.result-siren {
    font-size: 1.17em;
    font-weight: 700;
    color: #7b61ff;
    letter-spacing: 0.11em;
    margin-bottom: 0.13em;
    margin-top: 0.1em;
    text-transform: uppercase;
}
.result-title {
    font-size: 1.13em;
    font-weight: 600;
    color: #2d2d52;
    margin-bottom: 0.16em;
    text-transform: uppercase;
    letter-spacing: 0.07em;
}
.result-label {
    font-size: 0.88em;
    color: #7b7b98;
    font-weight: 400;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-right: 0.7em;
    display: inline-block;
    min-width: 84px;
    vertical-align: top;
}
.result-value {
    font-size: 1.06em;
    color: #222;
    font-weight: 400;
    letter-spacing: 0.02em;
    display: inline-block;
    vertical-align: top;
    word-break: break-word;
    white-space: pre-line;
    max-width: 230px;
}
.result-line {
    margin-bottom: 0.31em;
    display: flex;
    flex-direction: row;
    align-items: baseline;
    width: 100%;
}
@media (max-width: 1100px) {
    .results-row { gap: 1.1em;}
    .result-card {min-width: 260px; max-width: 99vw;}
}
@media (max-width: 768px) {
    .results-row { flex-wrap: wrap; gap: 0.8em;}
    .result-card {min-width: 96vw; max-width: 99vw;}
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="titre">TALKENTREPRISE</div>', unsafe_allow_html=True)

if "results" not in st.session_state:
    st.session_state.results = []
if "total_results" not in
