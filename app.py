import streamlit as st
import requests
import html

st.set_page_config(page_title="TALKENTREPRISE", page_icon="💬", layout="centered")

st.markdown("""
<style>
body, html, [class*="css"] {
    font-family: 'Avenir Next', Arial, sans-serif !important;
    border-radius: 24px !important;
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
.cards-row-scroll {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    overflow-x: auto;
    gap: 2.1em;
    margin-bottom: 1.2em;
    padding-bottom: 0.5em;
    padding-left: 0.1em;
    padding-right: 0.1em;
    scrollbar-width: thin;
    scrollbar-color: #ececf3 #f9f9fb;
}
.cards-row-scroll::-webkit-scrollbar {
    height: 8px;
    background: #f9f9fb;
}
.cards-row-scroll::-webkit-scrollbar-thumb {
    background: #ececf3;
    border-radius: 8px;
}
.result-card {
    background: #fff;
    border-radius: 24px;
    box-shadow: 0 4px 24px 0 rgba(30,30,68,0.08), 0 1.5px 4px #ececf3;
    padding: 30px 34px 26px 34px;
    min-width: 320px;
    max-width: 370px;
    min-height: 190px;
    border: 1px solid #f2f2f6;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    word-break: break-word;
    margin-bottom: 1em;
    position: relative;
}
.result-index {
    position: absolute;
    top: 19px;
    right: 28px;
    font-family: 'Avenir Next', Arial, sans-serif !important;
    font-size: 0.98em;
    color: #b6b6c2;
    font-weight: 200;
    letter-spacing: 0.06em;
    text-align: right;
    z-index: 2;
    pointer-events: none;
    user-select: none;
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
    white-space: normal !important;
    max-width: 220px;
}
.result-line {
    margin-bottom: 0.31em;
    display: flex;
    flex-direction: row;
    align-items: baseline;
}
@media (max-width: 1100px) {
    .cards-row-scroll { gap: 1.1em;}
    .result-card {min-width: 220px; max-width: 99vw;}
}
@media (max-width: 768px) {
    .cards-row-scroll { gap: 0.8em;}
    .result-card {min-width: 94vw; max-width: 99vw;}
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="titre">TALKENTREPRISE</div>', unsafe_allow_html=True)

if "results" not in st.session_state:
    st.session_state.results = []
if "total_results" not in st.session_state:
    st.session_state.total_results = 0

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
        dirigeant = (d.get("denomination") or d.get("nom") or "") + (" (" + d.get("qualite") + ")" if d.get("qualite") else "")
    date_creation = result.get("date_creation", "")
    return {
        "siren": siren,
        "nom": nom,
        "categorie": categorie,
        "adresse": adresse,
        "dirigeant": dirigeant,
        "date_creation": date_creation,
    }

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

st.text_input("", key="input_text", label_visibility="collapsed", on_change=send_and_clear)

if st.session_state.total_results:
    st.markdown(
        f'<div class="totalresult-text">TotalResult {st.session_state.total_results}</div>',
        unsafe_allow_html=True
    )

# Affichage : horizontal scroll, index discret en haut à droite de chaque carte
if st.session_state.results:
    cards_html = '<div class="cards-row-scroll">'
    for idx, info in enumerate(st.session_state.results):
        cards_html += f"""
        <div class="result-card">
            <span class="result-index">Résultat {idx+1}</span>
            <div class="result-siren">{safe_escape(info['siren'])}</div>
            <div class="result-title">{safe_escape(info['nom'])}</div>
            <div class="result-line"><span class="result-label">Dirigeant</span><span class="result-value">{safe_escape(info['dirigeant'])}</span></div>
            <div class="result-line"><span class="result-label">Adresse</span><span class="result-value">{safe_escape(info['adresse'])}</span></div>
            <div class="result-line"><span class="result-label">Catégorie</span><span class="result-value">{safe_escape(info['categorie'])}</span></div>
            <div class="result-line"><span class="result-label">Date création</span><span class="result-value">{safe_escape(info['date_creation'])}</span></div>
        </div>
        """
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)
