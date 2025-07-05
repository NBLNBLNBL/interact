import streamlit as st
import html
from datetime import datetime

st.set_page_config(page_title="TALKENTREPRISE", page_icon="💬", layout="centered")

# CSS stylé, cartes centrées, largeur identique, hauteur dynamique, police Avenir Next extra-fin partout
st.markdown("""
<style>
body, html, [class*="css"] {
    font-family: 'Avenir Next', Arial, sans-serif !important;
    background: #f9f9fb !important;
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
.cards-row-center {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    overflow-x: auto;
    gap: 1.4em;
    justify-content: center;
    align-items: flex-start;
    margin-bottom: 1.2em;
    padding-bottom: 0.5em;
    padding-left: 0.2em;
    padding-right: 0.2em;
    scrollbar-width: thin;
    scrollbar-color: #ececf3 #f9f9fb;
}
.cards-row-center::-webkit-scrollbar {
    height: 8px;
    background: #f9f9fb;
}
.cards-row-center::-webkit-scrollbar-thumb {
    background: #ececf3;
    border-radius: 8px;
}
.result-card {
    background: #fff;
    border-radius: 24px;
    box-shadow: 0 4px 24px 0 rgba(30,30,68,0.08), 0 1.5px 4px #ececf3;
    padding: 22px 26px 18px 26px;
    min-width: 350px;
    max-width: 350px;
    width: 350px;
    border: 1px solid #f2f2f6;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    word-break: break-word;
    margin-bottom: 1em;
    position: relative;
    transition: box-shadow 0.2s;
}
.result-card:hover {
    box-shadow: 0 8px 32px 0 rgba(30,30,68,0.11), 0 3px 8px #ececf3;
}
.result-header-row {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 0.11em;
}
.result-siren {
    font-size: 1.11em;
    font-weight: 700;
    color: #7b61ff;
    letter-spacing: 0.11em;
    text-transform: uppercase;
    font-family: 'Avenir Next', Arial, sans-serif !important;
}
.result-index {
    font-family: 'Avenir Next', Arial, sans-serif !important;
    font-size: 0.99em;
    color: #b6b6c2;
    font-weight: 200;
    letter-spacing: 0.07em;
    text-align: right;
    margin-left: 1em;
    white-space: nowrap;
    pointer-events: none;
    user-select: none;
}
.result-title {
    font-size: 1.08em;
    font-weight: 600;
    color: #2d2d52;
    margin-bottom: 0.13em;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    font-family: 'Avenir Next', Arial, sans-serif !important;
}
.result-label {
    font-size: 0.85em;
    color: #7b7b98;
    font-weight: 400;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-right: 0.7em;
    display: inline-block;
    min-width: 78px;
    vertical-align: top;
    font-family: 'Avenir Next', Arial, sans-serif !important;
}
.result-value {
    font-size: 1.02em;
    color: #222;
    font-weight: 400;
    letter-spacing: 0.02em;
    display: inline-block;
    vertical-align: top;
    word-break: break-word;
    white-space: normal !important;
    min-width: 30px;
    max-width: 250px;
    font-family: 'Avenir Next', Arial, sans-serif !important;
}
.result-line {
    margin-bottom: 0.16em;
    display: flex;
    flex-direction: row;
    align-items: baseline;
}
.stTextInput>div>input {
    font-family: 'Avenir Next', Arial, sans-serif !important;
    font-size: 1.07em;
    font-weight: 200 !important;
    color: #7b7b98 !important;
    background: #f9f9fb !important;
    border-radius: 18px !important;
    border: 1.2px solid #e4e4f5 !important;
    padding: 0.7em 1.1em !important;
}
@media (max-width: 1100px) {
    .cards-row-center { gap: 1em;}
    .result-card {min-width: 220px; max-width: 92vw; width: 92vw;}
    .result-value {max-width: 50vw;}
}
@media (max-width: 768px) {
    .cards-row-center { gap: 0.7em;}
    .result-card {min-width: 89vw; max-width: 99vw; width: 99vw;}
    .result-value {max-width: 70vw;}
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="titre">TALKENTREPRISE</div>', unsafe_allow_html=True)
