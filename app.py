import streamlit as st
import requests
import json

st.set_page_config(page_title="TALKENTREPRISE", page_icon="💬", layout="centered")

# Apple-style CSS pour vignettes en ligne, centrées, responsive
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
    text-transform: uppercase;
}
.results-row {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 1.5em;
    margin-bottom: 1.2em;
}
.result-card {
    background: #f9f9fb;
    border-radius: 20px;
    box-shadow: 0 4px 24px 0 rgba(30,30,68,0.08), 0 1.5px 4px #ececf3;
    padding: 22px 26px 18px 26px;
    min-width: 235px;
    max-width: 270px;
    min-height: 220px;
    border: 1px solid #f2f2f6;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
}
.result-siren {
    font-size: 1.15em;
    font-weight: 700;
    color: #7b61ff;
    letter-spacing: 0.09em;
    margin-bottom: 0.11em;
    margin-top: 0.1em;
    text-transform: uppercase;
}
.result-title {
    font-size: 1.09em;
    font-weight: 600;
    color: #2d2d52;
    margin-bottom: 0.18em;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.result-label {
    font-size: 0.83em;
    color: #7b7b98;
    font-weight: 400;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-right: 0.7em;
    display: inline-block;
    min-width: 70px;
}
.result-value {
    font-size: 1em;
    color: #222;
    font-weight: 400;
    letter-spacing: 0.02em;
    display: inline-block;
}
.result-line {
    margin-bottom: 0.36em;
}
@media (max-width: 1000px) {
    .results-row { gap: 1em;}
    .result-card {min-width: 185px; max-width: 98vw;}
}
@media (max-width: 768px) {
    .results-row { flex-wrap: wrap; gap: 0.8em;}
    .result-card {min-width: 97vw; max-width: 98vw;}
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="titre">TALKENTREPRISE</div>', unsafe_allow_html=True)

if "results" not in st.session_state:
    st.session_state.results = []

def extract_info(result):
    siren = result.get("siren", "")
    nom = result.get("nom_complet", "") or result.get("nom_raison_sociale", "")
    categorie = result.get("categorie_entreprise", "")
    activite = result.get("activite_principale", "")
    siege = result.get("siege", {})
    adresse = siege.get("geo_adresse") or siege.get("adresse", "")
    cp = siege.get("code_postal", "")
    ville = siege.get("libelle_commune", "")
    dirigeants = result.get("dirigeants", [])
    dirigeant = ""
    if dirigeants:
        d = dirigeants[0]
        dirigeant = (d.get("denomination") or d.get("nom") or "") + (" (" + d.get("qualite") + ")" if d.get("qualite") else "")
    siret = siege.get("siret", "")
    date_creation = result.get("date_creation", "")
    effectif = siege.get("tranche_effectif_salarie") or result.get("tranche_effectif_salarie") or ""
    return {
        "siren": siren,
        "nom": nom,
        "categorie": categorie,
        "activite": activite,
        "adresse": adresse,
        "cp": cp,
        "ville": ville,
        "dirigeant": dirigeant,
        "siret": siret,
        "date_creation": date_creation,
        "effectif": effectif
    }

def send_and_clear():
    user_input = st.session_state.input_text
    if user_input.strip():
        webhook_url = "https://leroux.app.n8n.cloud/webhook/dd642072-9735-4406-90c7-5a7a8a7ab9ea"
        try:
            resp = requests.post(webhook_url, json={"query": user_input}, timeout=15)
            try:
                data = resp.json()
                # Compatible avec une réponse enveloppée (cf. ton exemple)
                if isinstance(data, list) and "results" in data[0]:
                    res_list = data[0]["results"]
                elif "results" in data:
                    res_list = data["results"]
                else:
                    res_list = []
                st.session_state.results = [extract_info(r) for r in res_list]
            except Exception:
                st.session_state.results = []
        except Exception:
            st.session_state.results = []
    st.session_state.input_text = ""

st.text_input("", key="input_text", label_visibility="collapsed", on_change=send_and_clear)

# Affichage des résultats en ligne, flex, centrés
if st.session_state.results:
    cards_html = '<div class="results-row">'
    for info in st.session_state.results:
        cards_html += f"""
        <div class="result-card">
            <div class="result-siren">{info['siren']}</div>
            <div class="result-title">{info['nom']}</div>
            <div class="result-line"><span class="result-label">Dirigeant</span><span class="result-value">{info['dirigeant']}</span></div>
            <div class="result-line"><span class="result-label">Adresse</span><span class="result-value">{info['adresse']}</span></div>
            <div class="result-line"><span class="result-label">Activité</span><span class="result-value">{info['activite']}</span></div>
            <div class="result-line"><span class="result-label">Catégorie</span><span class="result-value">{info['categorie']}</span></div>
            <div class="result-line"><span class="result-label">Date création</span><span class="result-value">{info['date_creation']}</span></div>
        </div>
        """
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)
