import streamlit as st
import requests
import html
import streamlit.components.v1 as components

st.set_page_config(page_title="TALKENTREPRISE", page_icon="💬", layout="centered")

# CSS personnalisé avec défilement vertical et arrière-plan blanc pour le conteneur
html_style = """
<style>
body, html, [class*="css"] {
    font-family: 'Avenir Next', Arial, sans-serif !important;
    background: #ffffff !important;  /* Tout blanc */
    margin: 0;
    padding: 0;
}
.titre {
    font-size: 2.1rem;
    letter-spacing: 0.23em;
    font-weight: 200;
    text-align: center;
    margin: 1rem 0 1.2rem 0;
    text-transform: uppercase;
    color: #000;  /* en noir */
}
.totalresult-text {
    font-size: 0.97em;
    font-weight: 200;
    color: #b6b6c2;
    letter-spacing: 0.07em;
    text-align: center;
    margin-bottom: 1rem;
}
.input-container {
    text-align: center;
    margin-bottom: 1.2rem;
}
.cards-container {
    display: flex;
    flex-direction: column;         /* Passage en défilement vertical */
    gap: 1.5em;
    max-height: 500px;              /* Ajustez selon vos besoins */
    overflow-y: auto;
    padding: 0 1rem;
    margin-bottom: 1.2rem;
}
.cards-container::-webkit-scrollbar {
    width: 8px;
    background: #ffffff;
}
.cards-container::-webkit-scrollbar-thumb {
    background: #ececf3;
    border-radius: 8px;
}
.result-card {
    background: #fff;
    border-radius: 24px;
    box-shadow: 0 4px 24px rgba(30,30,68,0.08), 0 1.5px 4px #ececf3;
    padding: 22px 26px 18px 26px;
    min-width: 320px;
    width: 100%;
    max-width: 95vw;
    border: 1px solid #f2f2f6;
    display: flex;
    flex-direction: column;
    word-break: break-word;
    position: relative;
    margin: 0 auto;
}
.result-header-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 0.2em;
}
.result-siren {
    font-size: 1.11em;
    font-weight: 700;
    color: #7b61ff;
    letter-spacing: 0.11em;
    text-transform: uppercase;
}
.result-index {
    font-size: 0.99em;
    color: #b6b6c2;
    font-weight: 200;
    letter-spacing: 0.07em;
    text-align: right;
    white-space: nowrap;
}
.result-title {
    font-size: 1.08em;
    font-weight: 600;
    color: #2d2d52;
    margin-bottom: 0.2em;
    text-transform: uppercase;
    letter-spacing: 0.07em;
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
}
.result-value {
    font-size: 1.02em;
    color: #222;
    font-weight: 400;
    letter-spacing: 0.02em;
    display: inline-block;
    vertical-align: top;
    word-break: break-word;
    white-space: normal;
    max-width: 340px;
}
.result-line {
    margin-bottom: 0.18em;
    display: flex;
    align-items: baseline;
}
@media (max-width: 1100px) {
    .result-card { min-width: 180px; max-width: 98vw; }
    .result-value { max-width: 70vw; }
}
@media (max-width: 768px) {
    .result-card { min-width: 89vw; max-width: 99vw; }
    .result-value { max-width: 70vw; }
}
</style>
"""

def safe_escape(val):
    return html.escape(str(val)) if val is not None else ""

def extract_info(result):
    siren = result.get("siren", "")
    nom = result.get("nom_complet", "") or result.get("nom_raison_sociale", "")
    categorie = result.get("categorie_entreprise", "")
    siege = result.get("siege", {})
    adresse = siege.get("geo_adresse") or siege.get("adresse", "")
    dirigeants = result.get("dirigeants", [])
    dirigeant = ""
    if dirigeants:
        d = dirigeants[0]
        dirigeant = (d.get("denomination") or d.get("nom") or "") + (f" ({d.get('qualite')})" if d.get("qualite") else "")
    date_creation = result.get("date_creation", "")
    return {
        "siren": siren,
        "nom": nom,
        "categorie": categorie,
        "adresse": adresse,
        "dirigeant": dirigeant,
        "date_creation": date_creation,
    }

if "results" not in st.session_state:
    st.session_state.results = []
if "total_results" not in st.session_state:
    st.session_state.total_results = 0

def send_and_clear():
    user_input = st.session_state.input_text
    if user_input.strip():
        webhook_url = "https://leroux.app.n8n.cloud/webhook/dd642072-9735-4406-90c7-5a7a8a7ab9ea"
        try:
            resp = requests.post(webhook_url, json={"query": user_input}, timeout=15)
            try:
                data = resp.json()
                if isinstance(data, list) and "results" in data[0]:
                    res_list = data[0]["results"]
                    total = data[0].get("total_results", len(res_list))
                elif "results" in data:
                    res_list = data["results"]
                    total = data.get("total_results", len(res_list))
                else:
                    res_list = []
                    total = 0
                st.session_state.results = [extract_info(r) for r in res_list[:5]]
                st.session_state.total_results = total
            except Exception:
                st.session_state.results = []
                st.session_state.total_results = 0
        except Exception:
            st.session_state.results = []
            st.session_state.total_results = 0
    st.session_state.input_text = ""

# Place la barre de recherche sous le titre (sans subgroupes gris, fond blanc)
st.markdown('<div class="titre">TALKENTREPRISE</div>', unsafe_allow_html=True)
st.text_input("", key="input_text", label_visibility="collapsed", on_change=send_and_clear)

# Construction du HTML pour les cartes dans un conteneur vertical scrollable
cards_html = f"""
<html>
<head>
{html_style}
</head>
<body>
"""
if st.session_state.total_results:
    cards_html += f'<div class="totalresult-text">TotalResult {st.session_state.total_results}</div>'

if st.session_state.results:
    cards_html += '<div class="cards-container">'
    for idx, info in enumerate(st.session_state.results):
        cards_html += f"""
        <div class="result-card">
            <div class="result-header-row">
                <span class="result-siren">{safe_escape(info['siren'])}</span>
                <span class="result-index">Résultat {idx+1}</span>
            </div>
            <div class="result-title">{safe_escape(info['nom'])}</div>
            <div class="result-line">
                <span class="result-label">Dirigeant</span>
                <span class="result-value">{safe_escape(info['dirigeant'])}</span>
            </div>
            <div class="result-line">
                <span class="result-label">Adresse</span>
                <span class="result-value">{safe_escape(info['adresse'])}</span>
            </div>
            <div class="result-line">
                <span class="result-label">Catégorie</span>
                <span class="result-value">{safe_escape(info['categorie'])}</span>
            </div>
            <div class="result-line">
                <span class="result-label">Date création</span>
                <span class="result-value">{safe_escape(info['date_creation'])}</span>
            </div>
        </div>
        """
    cards_html += '</div>'
cards_html += "</body></html>"

# Intégration du HTML via st.components.html
components.html(cards_html, height=600)
