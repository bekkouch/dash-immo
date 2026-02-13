"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
L'Investissement Immobilier Locatif Intelligent — Dashboard Interactif
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Run with:  streamlit run app.py
Requires:  pip install streamlit plotly numpy pandas
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from dataclasses import dataclass

# ─────────────────────────────────────────────────────────────────────
# CONFIG & STYLING
# ─────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Immobilier Locatif Intelligent",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=DM+Serif+Display&display=swap');

    .stApp {
        font-family: 'DM Sans', sans-serif;
    }
    h1, h2, h3 { font-family: 'DM Serif Display', serif !important; }

    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        color: white;
    }
    .metric-card .label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #a0aec0;
        margin-bottom: 0.3rem;
    }
    .metric-card .value {
        font-family: 'DM Serif Display', serif;
        font-size: 2rem;
        color: #48bb78;
    }
    .metric-card .value.negative { color: #fc8181; }
    .metric-card .value.neutral  { color: #63b3ed; }
    .metric-card .sub {
        font-size: 0.75rem;
        color: #718096;
        margin-top: 0.25rem;
    }

    /* Info boxes */
    .concept-box {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        border-left: 4px solid #48bb78;
        border-radius: 0 12px 12px 0;
        padding: 1.2rem 1.5rem;
        margin: 1rem 0;
        color: #000000;
    }
    .concept-box h4 { color: #48bb78; margin: 0 0 0.5rem 0; }

    .strategy-box {
        background: linear-gradient(135deg, #1a1a2e, #2d1b69);
        border-left: 4px solid #b794f4;
        border-radius: 0 12px 12px 0;
        padding: 1.2rem 1.5rem;
        margin: 1rem 0;
        color: #000000;
    }
    .strategy-box h4 { color: #b794f4; margin: 0 0 0.5rem 0; }

    .warning-box {
        background: linear-gradient(135deg, #2d1f00, #3d2b00);
        border-left: 4px solid #f6ad55;
        border-radius: 0 12px 12px 0;
        padding: 1.2rem 1.5rem;
        margin: 1rem 0;
        color: #000000;
    }
    .warning-box h4 { color: #f6ad55; margin: 0 0 0.5rem 0; }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29, #302b63, #24243e);
    }
    section[data-testid="stSidebar"] * { color: #000000 !important; }

    .stTabs [data-baseweb="tab-list"] { gap: 0.5rem; }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.05) !important;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(72,187,120,0.15) !important;
        border-bottom-color: #48bb78 !important;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 12px;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)


def metric_card(label, value, sub="", css_class=""):
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">{label}</div>
        <div class="value {css_class}">{value}</div>
        <div class="sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)


def concept_box(title, text):
    st.markdown(f"""
    <div class="concept-box">
        <h4>📐 {title}</h4>
        <p>{text}</p>
    </div>
    """, unsafe_allow_html=True)


def strategy_box(title, text):
    st.markdown(f"""
    <div class="strategy-box">
        <h4>🎯 {title}</h4>
        <p>{text}</p>
    </div>
    """, unsafe_allow_html=True)


def warning_box(title, text):
    st.markdown(f"""
    <div class="warning-box">
        <h4>⚠️ {title}</h4>
        <p>{text}</p>
    </div>
    """, unsafe_allow_html=True)


PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#000000"),
    margin=dict(l=40, r=40, t=50, b=40),
    xaxis=dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.1)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.1)"),
)


# ─────────────────────────────────────────────────────────────────────
# SIDEBAR — GLOBAL PARAMETERS
# ─────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 🏠 Paramètres Globaux")
    st.markdown("---")

    st.markdown("### 💰 Le Bien")
    prix_achat = st.number_input("Prix d'achat (€)", 10_000, 1_000_000, 100_000, step=5_000)
    frais_notaire_pct = st.slider("Frais de notaire (%)", 0.0, 10.0, 7.5, 0.5)
    travaux = st.number_input("Travaux (€)", 0, 200_000, 5_000, step=1_000)
    surface_m2 = st.number_input("Surface (m²)", 9, 500, 40, step=1)

    st.markdown("### 🏦 Le Crédit")
    apport = st.number_input("Apport (€)", 0, 500_000, 0, step=1_000)
    taux_emprunt = st.slider("Taux d'emprunt (%)", 0.5, 6.0, 1.8, 0.1)
    duree_credit = st.slider("Durée du crédit (ans)", 5, 25, 20)
    assurance_emprunt_pct = st.slider("Assurance emprunteur (%/an)", 0.05, 0.60, 0.20, 0.01)

    st.markdown("### 🔑 La Location")
    loyer_mensuel_cc = st.number_input("Loyer mensuel CC (€)", 50, 10_000, 600, step=25)
    charges_copro_an = st.number_input("Charges copro / an (€)", 0, 15_000, 800, step=100)
    taxe_fonciere = st.number_input("Taxe foncière / an (€)", 0, 10_000, 700, step=50)
    assurance_pno = st.number_input("Assurance PNO / an (€)", 0, 2_000, 120, step=10)
    vacance_loc_mois = st.slider("Vacance locative (mois/an)", 0.0, 3.0, 0.5, 0.25)

    st.markdown("### 📊 Fiscalité")
    tmi = st.selectbox("Tranche Marginale d'Imposition", [0, 11, 30, 41, 45], index=2)
    prelevement_sociaux = 17.2
    regime_fiscal = st.selectbox("Régime fiscal", [
        "Nu — Micro-foncier (30%)",
        "Nu — Réel (Déficit foncier)",
        "Nu — Réel + Cosse Ancien",
        "Meublé LMNP — Micro-BIC (50%)",
        "Meublé LMNP — Réel Simplifié",
    ], index=4)


# ─────────────────────────────────────────────────────────────────────
# CORE CALCULATIONS
# ─────────────────────────────────────────────────────────────────────

frais_notaire = prix_achat * frais_notaire_pct / 100
investissement_total = prix_achat + frais_notaire + travaux
montant_emprunt = prix_achat + travaux - apport

# Mensualité (amortissement constant taux fixe)
taux_mensuel = taux_emprunt / 100 / 12
nb_mois = duree_credit * 12
if taux_mensuel > 0:
    mensualite = montant_emprunt * taux_mensuel / (1 - (1 + taux_mensuel) ** (-nb_mois))
else:
    mensualite = montant_emprunt / nb_mois

# Assurance emprunteur
assurance_emprunt_mensuel = montant_emprunt * assurance_emprunt_pct / 100 / 12

# Loyer net de vacance
loyer_annuel_cc = loyer_mensuel_cc * 12
loyer_effectif_an = loyer_mensuel_cc * (12 - vacance_loc_mois)
charges_locataire_an = charges_copro_an * 0.65  # part récup. estimée
loyer_nu_an = loyer_effectif_an - charges_locataire_an

# Rendements
rendement_brut = (loyer_annuel_cc / investissement_total) * 100
charges_totales_an = taxe_fonciere + (charges_copro_an * 0.35) + assurance_pno + travaux * 0.02  # 2% entretien
rendement_net_charges = ((loyer_effectif_an - charges_totales_an) / investissement_total) * 100

# Amortissement table (year by year)
capital_restant = montant_emprunt
yearly_data = []
for year in range(1, duree_credit + 1):
    interets_an = 0
    capital_rembourse_an = 0
    for m in range(12):
        interet_mois = capital_restant * taux_mensuel
        capital_mois = mensualite - interet_mois
        capital_restant -= capital_mois
        interets_an += interet_mois
        capital_rembourse_an += capital_mois

    # Fiscal computation
    charges_deductibles = interets_an + taxe_fonciere + assurance_pno + (charges_copro_an * 0.35)

    if "Micro-foncier" in regime_fiscal:
        base_imposable = loyer_nu_an * 0.70
        impots = base_imposable * (tmi / 100 + prelevement_sociaux / 100) if base_imposable > 0 else 0
    elif "Réel" in regime_fiscal and "Cosse" in regime_fiscal:
        abattement_cosse = 0.50  # Zone B2 social
        revenus_apres_cosse = loyer_nu_an * (1 - abattement_cosse)
        base_imposable = max(0, revenus_apres_cosse - charges_deductibles)
        impots = base_imposable * (tmi / 100 + prelevement_sociaux / 100)
    elif "Réel" in regime_fiscal and "Déficit" in regime_fiscal:
        base_imposable = loyer_nu_an - charges_deductibles
        if base_imposable < 0:
            deficit = abs(base_imposable)
            imputation_rg = min(deficit, 10700)
            impots = -imputation_rg * (tmi / 100)  # gain fiscal
        else:
            impots = base_imposable * (tmi / 100 + prelevement_sociaux / 100)
    elif "Micro-BIC" in regime_fiscal:
        base_imposable = loyer_effectif_an * 0.50
        impots = base_imposable * (tmi / 100 + prelevement_sociaux / 100) if base_imposable > 0 else 0
    elif "LMNP" in regime_fiscal and "Réel" in regime_fiscal:
        amortissement = (prix_achat * 0.90) / 30  # 90% sur 30 ans
        amort_meubles = 3000 / 7  # meubles sur 7 ans
        total_amort = amortissement + (amort_meubles if year <= 7 else 0)
        base_imposable = max(0, loyer_effectif_an - charges_deductibles - total_amort)
        impots = base_imposable * (tmi / 100 + prelevement_sociaux / 100)
    else:
        impots = 0

    # Cash-flow
    total_mensualite = mensualite + assurance_emprunt_mensuel
    depenses_an = total_mensualite * 12 + charges_totales_an + max(0, impots)
    cashflow_an = loyer_effectif_an - depenses_an
    if impots < 0:
        cashflow_an -= impots  # gain fiscal positif

    yearly_data.append({
        "Année": year,
        "Loyer Effectif": loyer_effectif_an,
        "Mensualités Crédit": total_mensualite * 12,
        "Intérêts": interets_an,
        "Capital Remboursé": capital_rembourse_an,
        "Capital Restant Dû": max(0, capital_restant),
        "Charges": charges_totales_an,
        "Impôts": max(0, impots),
        "Gain Fiscal": abs(min(0, impots)),
        "Cash-flow Annuel": cashflow_an,
        "Cash-flow Mensuel": cashflow_an / 12,
    })

df = pd.DataFrame(yearly_data)

# Net-net
impots_an1 = df.iloc[0]["Impôts"] - df.iloc[0]["Gain Fiscal"]
rendement_net_net = ((loyer_effectif_an - charges_totales_an - impots_an1) / investissement_total) * 100

# Cash-flow mensuel moyen
cashflow_mensuel = df.iloc[0]["Cash-flow Mensuel"]


# ─────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────

st.markdown("""
<div style="text-align:center; padding: 1.5rem 0 0.5rem;">
    <h1 style="font-size:2.4rem; margin-bottom:0.2rem;">
        🏠 L'Investissement Immobilier Locatif Intelligent
    </h1>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────

tabs = st.tabs([
    "📊 Rendements & Cash-flow",
    "🎯 Rendement Entrepreneurial",
    "🏦 Financement & Levier",
    "📋 Fiscalité",
    "⚖️ Taux de Sérénité",
    "🛡️ Gestion des Risques",
    "📈 Stratégies d'Investissement",
    "🔧 Outils DCF & Comparables",
])


# ═══════════════════════════════════════════════════════════════
# TAB 1 — RENDEMENTS & CASH-FLOW
# ═══════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown("## Rendements Locatifs & Cash-flow")
    concept_box(
        "Les 3 niveaux de rendement (Chapitre A.1)",
        "Le rendement <b>brut</b> est un premier filtre rapide. Le rendement <b>net de charges</b> "
        "affine. Mais c'est le rendement <b>net-net</b> (après impôts) qui compte vraiment — "
        "c'est ce qui atterrit dans votre poche."
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Rendement Brut", f"{rendement_brut:.2f} %",
                     f"Loyer CC / Investissement total", "neutral")
    with col2:
        metric_card("Rendement Net Charges", f"{rendement_net_charges:.2f} %",
                     "Après charges non récupérables")
    with col3:
        css = "" if rendement_net_net > 0 else "negative"
        metric_card("Rendement Net-Net", f"{rendement_net_net:.2f} %",
                     "Après impôts et prélèvements sociaux", css)
    with col4:
        css = "" if cashflow_mensuel >= 0 else "negative"
        signe = "+" if cashflow_mensuel >= 0 else ""
        metric_card("Cash-flow Mensuel", f"{signe}{cashflow_mensuel:.0f} €",
                     "Année 1 — Ce qui reste en poche", css)

    st.markdown("---")

    concept_box(
        "Cash-flow positif = Clé de l'investisseur intelligent (Chapitre B.1)",
        "Un cash-flow positif vous permet de : <b>(1)</b> profiter de votre investissement dès maintenant, "
        "<b>(2)</b> enchaîner les investissements car les banques vous prêteront plus facilement, "
        "<b>(3)</b> vous protéger contre les imprévus. Oubliez « l'effort d'épargne » !"
    )

    # Cash-flow evolution chart
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        fig_cf = go.Figure()
        colors = ["#48bb78" if v >= 0 else "#fc8181" for v in df["Cash-flow Annuel"]]
        fig_cf.add_trace(go.Bar(
            x=df["Année"], y=df["Cash-flow Annuel"],
            marker_color=colors, name="Cash-flow",
            hovertemplate="Année %{x}<br>Cash-flow: %{y:,.0f} €<extra></extra>"
        ))
        fig_cf.update_layout(
            title="Évolution du Cash-flow Annuel",
            yaxis_title="€",
            **PLOTLY_LAYOUT
        )
        fig_cf.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.3)")
        st.plotly_chart(fig_cf, use_container_width=True)

    with col_chart2:
        fig_pie = go.Figure(data=[go.Pie(
            labels=["Loyer Effectif", "Mensualités Crédit", "Charges", "Impôts"],
            values=[
                loyer_effectif_an,
                (mensualite + assurance_emprunt_mensuel) * 12,
                charges_totales_an,
                max(0, df.iloc[0]["Impôts"] - df.iloc[0]["Gain Fiscal"])
            ],
            marker=dict(colors=["#48bb78", "#fc8181", "#f6ad55", "#b794f4"]),
            hole=0.5,
            textinfo="label+percent",
            hovertemplate="%{label}: %{value:,.0f} €<extra></extra>"
        )])
        fig_pie.update_layout(
            title="Décomposition Année 1",
            **PLOTLY_LAYOUT,
            showlegend=False,
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # Waterfall chart
    st.markdown("#### 🔍 Cascade du Cash-flow Mensuel (Année 1)")
    loyer_m = loyer_effectif_an / 12
    mensualite_tot = mensualite + assurance_emprunt_mensuel
    charges_m = charges_totales_an / 12
    impots_m = max(0, df.iloc[0]["Impôts"] - df.iloc[0]["Gain Fiscal"]) / 12

    fig_wf = go.Figure(go.Waterfall(
        name="Cash-flow",
        orientation="v",
        x=["Loyer Effectif", "- Mensualité Crédit", "- Charges", "- Impôts", "= Cash-flow"],
        y=[loyer_m, -mensualite_tot, -charges_m, -impots_m, 0],
        measure=["absolute", "relative", "relative", "relative", "total"],
        connector={"line": {"color": "rgba(255,255,255,0.2)"}},
        increasing={"marker": {"color": "#48bb78"}},
        decreasing={"marker": {"color": "#fc8181"}},
        totals={"marker": {"color": "#63b3ed" if cashflow_mensuel >= 0 else "#fc8181"}},
        textposition="outside",
        text=[f"{loyer_m:,.0f}€", f"-{mensualite_tot:,.0f}€", f"-{charges_m:,.0f}€",
              f"-{impots_m:,.0f}€", f"{cashflow_mensuel:,.0f}€"],
    ))
    fig_wf.update_layout(
        title="",
        yaxis_title="€ / mois",
        showlegend=False,
        **PLOTLY_LAYOUT
    )
    st.plotly_chart(fig_wf, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# TAB 2 — RENDEMENT ENTREPRENEURIAL
# ═══════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown("## Rendement Entrepreneurial (Chapitre B.2)")
    concept_box(
        "Rendement = Capital + Entrepreneurial (Piketty / Delagrandanne)",
        "Le rendement du capital tourne historiquement autour de <b>5%</b>. "
        "Pour atteindre les <b>10%</b> nécessaires au cash-flow positif, "
        "il faut ajouter du <b>rendement entrepreneurial</b> : travaux, optimisation fiscale, "
        "reconfiguration, meilleure exploitation… <br><br>"
        "<b>10% = 5% rendement capital + 5% rendement entrepreneurial</b>"
    )

    st.markdown("### 🔨 Simulateur de Rendement Entrepreneurial")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Sources de rendement entrepreneurial")
        gain_travaux = st.number_input("Gain travaux (plus-value créée - coût) (€)", 0, 100_000, 5_000, step=500)
        gain_reconfig = st.number_input("Gain reconfiguration (ex: T1→T2) (€/an loyer sup.)", 0, 12_000, 1_200, step=100)
        gain_fiscal_an = st.number_input("Gain fiscal annuel estimé (€)", 0, 20_000, 1_500, step=100)
        gain_equipement = st.number_input("Gain équipements (€/an loyer sup.)", 0, 6_000, 600, step=50)

    with col2:
        total_gain_an = gain_reconfig + gain_fiscal_an + gain_equipement
        rdt_base = 5.0
        rdt_entrepreneurial = (total_gain_an / investissement_total) * 100
        rdt_total = rdt_base + rdt_entrepreneurial

        metric_card("Rendement Capital (base)", f"{rdt_base:.1f} %", "Rendement passif sans effort", "neutral")
        metric_card("Rendement Entrepreneurial", f"+{rdt_entrepreneurial:.2f} %",
                     f"Travail supplémentaire → +{total_gain_an:,.0f} €/an")
        metric_card("Rendement Total Estimé", f"{rdt_total:.2f} %",
                     "Capital + Entrepreneurial", "" if rdt_total >= 8 else "negative")

    # ROI equipment chart
    st.markdown("### ⏱️ Temps de Retour sur Équipements (Exemples vécus)")
    equip_data = pd.DataFrame({
        "Équipement": ["Cuisine équipée", "Lave-linge", "Parquet PVC", "Meuble sous-vasque",
                        "Peinture neuve", "Double vitrage"],
        "Coût (€)": [1000, 270, 600, 250, 800, 2500],
        "Loyer sup. (€/mois)": [50, 30, 15, 10, 20, 15],
    })
    equip_data["Retour (mois)"] = equip_data["Coût (€)"] / equip_data["Loyer sup. (€/mois)"]

    fig_equip = go.Figure(go.Bar(
        x=equip_data["Équipement"],
        y=equip_data["Retour (mois)"],
        marker_color=["#48bb78" if v < 24 else "#f6ad55" for v in equip_data["Retour (mois)"]],
        text=[f'{v:.0f} mois' for v in equip_data["Retour (mois)"]],
        textposition="outside",
    ))
    fig_equip.update_layout(
        title="Temps de retour sur investissement par équipement",
        yaxis_title="Mois",
        **PLOTLY_LAYOUT,
    )
    fig_equip.add_hline(y=24, line_dash="dash", line_color="#f6ad55",
                         annotation_text="Seuil 2 ans", annotation_position="top right")
    st.plotly_chart(fig_equip, use_container_width=True)

    strategy_box("Les 4 styles gagnants de rendement entrepreneurial", """
    <b>1. Travaux dans grandes agglos</b> — Acheter décoté, rénover, LMNP → rendement brut 8-10%<br>
    <b>2. Fort rendement zone rurale</b> — Immeubles de rapport, 12-15% brut, gestion active<br>
    <b>3. Pinel « non-pigeon »</b> — Maître d'ouvrage soi-même (terrain + construction)<br>
    <b>4. Optimisation fiscale</b> — Déficit foncier, Cosse Ancien, LMNP réel simplifié
    """)


# ═══════════════════════════════════════════════════════════════
# TAB 3 — FINANCEMENT & LEVIER
# ═══════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown("## Financement & Effet de Levier (Chapitres A.3, C.3)")

    concept_box(
        "L'Effet de Levier",
        "L'effet de levier = différence positive entre le rendement de votre investissement "
        "et le taux du crédit. Emprunter à 1.8% pour placer à 8% = excellente opération. "
        "Plus le différentiel est grand, plus vous vous enrichissez."
    )

    col1, col2, col3 = st.columns(3)
    differentiel = rendement_brut - taux_emprunt
    with col1:
        metric_card("Taux d'emprunt", f"{taux_emprunt:.2f} %", "Taux fixe négocié")
    with col2:
        metric_card("Rendement brut", f"{rendement_brut:.2f} %", "Du bien acheté", "neutral")
    with col3:
        css = "" if differentiel > 0 else "negative"
        metric_card("Différentiel (Levier)", f"{differentiel:=+.2f} %",
                     "Rendement - Taux emprunt = enrichissement", css)

    st.markdown("---")

    # Durée optimale du crédit
    st.markdown("### 📏 Impact de la Durée du Crédit sur le Cash-flow")
    warning_box("Oubliez les méthodes de papa ! (Chapitre C.3)",
                "Avec des taux bas, la durée optimale est <b>20 ans</b>. "
                "Moins long = cash-flow trop dégradé. 25 ans = trop peu de capital remboursé au début.")

    durees = list(range(10, 26))
    cashflows_by_duree = []
    for d in durees:
        n = d * 12
        if taux_mensuel > 0:
            mens = montant_emprunt * taux_mensuel / (1 - (1 + taux_mensuel) ** (-n))
        else:
            mens = montant_emprunt / n
        mens_tot = mens + assurance_emprunt_mensuel
        cf = loyer_effectif_an / 12 - mens_tot - charges_totales_an / 12
        cashflows_by_duree.append(cf)

    fig_duree = go.Figure()
    colors_dur = ["#48bb78" if v >= 0 else "#fc8181" for v in cashflows_by_duree]
    fig_duree.add_trace(go.Bar(
        x=durees, y=cashflows_by_duree,
        marker_color=colors_dur,
        text=[f"{v:+.0f}€" for v in cashflows_by_duree],
        textposition="outside",
    ))
    fig_duree.add_vline(x=20, line_dash="dash", line_color="#63b3ed",
                         annotation_text="Durée optimale: 20 ans")
    fig_duree.add_hline(y=0, line_dash="dot", line_color="rgba(255,255,255,0.3)")
    fig_duree.update_layout(
        title="Cash-flow mensuel (avant impôts) selon la durée du crédit",
        xaxis_title="Durée (ans)", yaxis_title="€ / mois",
        **PLOTLY_LAYOUT,
    )
    st.plotly_chart(fig_duree, use_container_width=True)

    # Taux d'endettement — 2 méthodes
    st.markdown("### 🏦 Deux méthodes de calcul du taux d'endettement")
    salaire_net = st.number_input("Salaire net mensuel (€)", 500, 50_000, 2_500, step=100)

    col1, col2 = st.columns(2)
    loyer_70 = loyer_mensuel_cc * 0.70  # banques retiennent 70%

    # Méthode 1 — Non-compensation
    endettement_nc = (mensualite + assurance_emprunt_mensuel) / (salaire_net + loyer_70) * 100
    # Méthode 2 — Compensation
    endettement_comp = max(0, (mensualite + assurance_emprunt_mensuel - loyer_70)) / salaire_net * 100

    with col1:
        css = "" if endettement_nc < 33 else "negative"
        metric_card("Méthode Non-Compensation", f"{endettement_nc:.1f} %",
                     "Mensualité / (Salaire + 70% Loyers) — Méthode basique", css)
    with col2:
        css = "" if endettement_comp < 33 else "negative"
        metric_card("Méthode Compensation", f"{endettement_comp:.1f} %",
                     "(Mensualité - 70% Loyers) / Salaire — Pour investisseurs confirmés", css)

    concept_box("La boule de neige (Chapitre C.3)",
                "Avec un cash-flow positif et la méthode de compensation, chaque investissement "
                "augmente à peine votre taux d'endettement → vous pouvez <b>enchaîner les opérations</b>.")

    # Coût réel du crédit locatif vs RP
    st.markdown("### 💡 Le Crédit Locatif coûte moins cher qu'un Crédit RP")
    taux_fictif = taux_emprunt * (1 - (tmi / 100 + prelevement_sociaux / 100))
    col1, col2 = st.columns(2)
    with col1:
        metric_card("Coût réel — Résidence Principale", f"{taux_emprunt:.2f} %", "Taux nominal")
    with col2:
        metric_card("Coût réel — Investissement Locatif", f"{taux_fictif:.2f} %",
                     f"Après déduction fiscale (TMI {tmi}% + PS {prelevement_sociaux}%)")


# ═══════════════════════════════════════════════════════════════
# TAB 4 — FISCALITÉ
# ═══════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown("## Optimisation Fiscale (Chapitre D.5)")

    concept_box(
        "3 voies pour adoucir la fiscalité",
        "<b>1.</b> Déficit foncier (travaux déductibles, plafond 10 700 €/an sur revenu global)<br>"
        "<b>2.</b> Loi Cosse Ancien (abattement 15-85% selon zone et type, cumulable avec déficit foncier)<br>"
        "<b>3.</b> LMNP Réel Simplifié (amortissement comptable du bien → fiscalité quasi nulle)"
    )

    st.markdown(f"### Régime sélectionné : `{regime_fiscal}`")

    # Compare all regimes
    st.markdown("### 📊 Comparaison des régimes fiscaux (Année 1)")
    regimes = {
        "Micro-foncier": loyer_nu_an * 0.70 * (tmi / 100 + prelevement_sociaux / 100),
        "Réel (Déf. Foncier)": max(0, (loyer_nu_an - (df.iloc[0]["Intérêts"] + taxe_fonciere + assurance_pno + charges_copro_an * 0.35))) * (tmi / 100 + prelevement_sociaux / 100),
        "Réel + Cosse B2 Social": max(0, loyer_nu_an * 0.50 - (df.iloc[0]["Intérêts"] + taxe_fonciere + assurance_pno + charges_copro_an * 0.35)) * (tmi / 100 + prelevement_sociaux / 100),
        "Micro-BIC (Meublé)": loyer_effectif_an * 0.50 * (tmi / 100 + prelevement_sociaux / 100),
        "LMNP Réel": max(0, loyer_effectif_an - (df.iloc[0]["Intérêts"] + taxe_fonciere + assurance_pno + charges_copro_an * 0.35 + prix_achat * 0.90 / 30 + 3000 / 7)) * (tmi / 100 + prelevement_sociaux / 100),
    }

    fig_fisc = go.Figure(go.Bar(
        x=list(regimes.keys()),
        y=list(regimes.values()),
        marker_color=["#fc8181", "#f6ad55", "#48bb78", "#63b3ed", "#b794f4"],
        text=[f"{v:,.0f} €" for v in regimes.values()],
        textposition="outside",
    ))
    fig_fisc.update_layout(
        title="Impôts + Prélèvements sociaux par régime (Année 1)",
        yaxis_title="€ / an",
        **PLOTLY_LAYOUT,
    )
    st.plotly_chart(fig_fisc, use_container_width=True)

    # Cash-flow comparison
    st.markdown("### 💰 Cash-flow Mensuel résultant par régime")
    cf_by_regime = {}
    base_cf_before_tax = loyer_effectif_an / 12 - (mensualite + assurance_emprunt_mensuel) - charges_totales_an / 12
    for name, tax in regimes.items():
        cf_by_regime[name] = base_cf_before_tax - tax / 12

    fig_cf_reg = go.Figure(go.Bar(
        x=list(cf_by_regime.keys()),
        y=list(cf_by_regime.values()),
        marker_color=["#48bb78" if v >= 0 else "#fc8181" for v in cf_by_regime.values()],
        text=[f"{v:+,.0f} €" for v in cf_by_regime.values()],
        textposition="outside",
    ))
    fig_cf_reg.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.3)")
    fig_cf_reg.update_layout(
        title="Cash-flow mensuel selon le régime fiscal",
        yaxis_title="€ / mois",
        **PLOTLY_LAYOUT,
    )
    st.plotly_chart(fig_cf_reg, use_container_width=True)

    # Deficit foncier simulator
    st.markdown("### 🔧 Simulateur Déficit Foncier")
    col1, col2 = st.columns(2)
    with col1:
        montant_travaux_df = st.number_input("Montant des travaux déductibles (€)", 0, 100_000, 10_000, step=1_000)
        revenus_fonciers_existants = st.number_input("Revenus fonciers préexistants (€/an)", 0, 50_000, 3_000, step=500)
    with col2:
        deficit = montant_travaux_df - loyer_nu_an - revenus_fonciers_existants
        if deficit > 0:
            imputation_foncier = min(loyer_nu_an + revenus_fonciers_existants, montant_travaux_df)
            gain_foncier = imputation_foncier * (tmi / 100 + prelevement_sociaux / 100)
            imputation_rg = min(deficit, 10_700)
            gain_rg = imputation_rg * tmi / 100
            report = max(0, deficit - 10_700)
            metric_card("Déficit Foncier Créé", f"{deficit:,.0f} €", "")
            metric_card("Gain Fiscal Total (Année N)", f"{gain_foncier + gain_rg:,.0f} €",
                         f"Sur fonciers: {gain_foncier:,.0f}€ + Sur revenu global: {gain_rg:,.0f}€")
            metric_card("Coût Net des Travaux", f"{montant_travaux_df - gain_foncier - gain_rg:,.0f} €",
                         f"Report restant: {report:,.0f}€ (sur 10 ans)")
        else:
            metric_card("Pas de déficit", f"{abs(deficit):,.0f} € de bénéfice foncier",
                         "Augmentez les travaux ou réduisez les revenus fonciers", "negative")


# ═══════════════════════════════════════════════════════════════
# TAB 5 — TAUX DE SÉRÉNITÉ
# ═══════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown("## Taux de Sérénité (Chapitre B.2)")

    concept_box(
        "Le corollaire au rendement entrepreneurial",
        "Plus vous poussez le rendement, plus l'énergie augmente (exponentiellement dans la zone haute) "
        "et plus le taux de sérénité baisse. La zone idéale est la <b>droite de la zone médiane</b> : "
        "« petit effort, gros résultat »."
    )

    # Interactive serenity chart
    x_rdt = np.linspace(3, 18, 200)
    # Serenity: starts high, linear drop, then accelerates
    serenite = np.piecewise(x_rdt,
        [x_rdt < 5, (x_rdt >= 5) & (x_rdt <= 10), x_rdt > 10],
        [lambda x: 90 - (x - 3) * 2,
         lambda x: 86 - (x - 5) * 6,
         lambda x: 56 - (x - 10) * 8 - (x - 10) ** 1.5 * 2]
    )
    serenite = np.clip(serenite, 5, 95)

    # Energy: starts low, linear, then exponential
    energie = np.piecewise(x_rdt,
        [x_rdt < 5, (x_rdt >= 5) & (x_rdt <= 10), x_rdt > 10],
        [lambda x: 10 + (x - 3) * 3,
         lambda x: 16 + (x - 5) * 8,
         lambda x: 56 + (x - 10) * 12 + (x - 10) ** 2 * 3]
    )
    energie = np.clip(energie, 5, 100)

    fig_serenite = go.Figure()
    fig_serenite.add_trace(go.Scatter(
        x=x_rdt, y=serenite, name="Taux de Sérénité",
        line=dict(color="#48bb78", width=3),
        fill="tozeroy", fillcolor="rgba(72,187,120,0.1)"
    ))
    fig_serenite.add_trace(go.Scatter(
        x=x_rdt, y=energie, name="Énergie à Déployer",
        line=dict(color="#fc8181", width=3),
        fill="tozeroy", fillcolor="rgba(252,129,129,0.1)"
    ))

    # Zone annotations
    fig_serenite.add_vrect(x0=3, x1=5, fillcolor="rgba(99,179,237,0.08)", line_width=0,
                            annotation_text="Rendement<br>Nominal", annotation_position="top")
    fig_serenite.add_vrect(x0=5, x1=10, fillcolor="rgba(72,187,120,0.08)", line_width=0,
                            annotation_text="Zone Idéale<br>Petit effort → Gros résultat",
                            annotation_position="top")
    fig_serenite.add_vrect(x0=10, x1=18, fillcolor="rgba(252,129,129,0.08)", line_width=0,
                            annotation_text="Zone Intensive<br>Gros effort requis",
                            annotation_position="top")

    # Current position
    fig_serenite.add_vline(x=rendement_brut, line_dash="dash", line_color="#b794f4",
                            annotation_text=f"Votre bien: {rendement_brut:.1f}%")

    fig_serenite.update_layout(
        title="Taux de Sérénité vs Énergie selon le Rendement Brut",
        xaxis_title="Rendement Brut (%)",
        yaxis_title="%",
        **PLOTLY_LAYOUT,
        legend=dict(x=0.7, y=0.95),
    )
    st.plotly_chart(fig_serenite, use_container_width=True)

    # Serenity by property type
    st.markdown("### 🏘️ Taux de sérénité par type de bien")
    types = pd.DataFrame({
        "Type": ["Maison T4+", "T3", "T2 centre-ville", "T1/Studio", "Colocation", "Immeuble rapport", "Meublé tourisme"],
        "Rdt Brut Typique (%)": [5, 5.5, 7, 8, 10, 12, 14],
        "Sérénité": [85, 75, 70, 55, 45, 35, 25],
        "Turnover": ["Très faible", "Faible", "Moyen", "Élevé", "Élevé", "Variable", "Très élevé"],
    })
    fig_types = go.Figure()
    fig_types.add_trace(go.Scatter(
        x=types["Rdt Brut Typique (%)"], y=types["Sérénité"],
        mode="markers+text",
        text=types["Type"],
        textposition="top center",
        marker=dict(size=types["Rdt Brut Typique (%)"] * 5, color="#b794f4", opacity=0.7),
        textfont=dict(color="#000000", size=11),
    ))
    fig_types.update_layout(
        title="Rendement vs Sérénité par type de bien",
        xaxis_title="Rendement Brut Typique (%)",
        yaxis_title="Taux de Sérénité (%)",
        **PLOTLY_LAYOUT,
    )
    st.plotly_chart(fig_types, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# TAB 6 — GESTION DES RISQUES
# ═══════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown("## Gestion des Risques (Chapitre B.3)")

    warning_box(
        "Regarder vers le bas plutôt que le haut",
        "L'investisseur intelligent ne base <b>jamais</b> la réussite sur une hausse future des prix. "
        "Il achète en dessous du prix de marché pour se créer une <b>marge de sécurité</b>."
    )

    # Stress test
    st.markdown("### 🔬 Stress Test de votre investissement")
    col1, col2 = st.columns(2)
    with col1:
        stress_vacance = st.slider("Vacance locative stress (mois/an)", 0.0, 6.0, 2.0, 0.5)
        stress_loyer = st.slider("Baisse des loyers (%)", 0, 30, 10, 5)
        stress_charges = st.slider("Hausse des charges (%)", 0, 50, 20, 5)
        stress_impots = st.slider("Hausse fiscalité (%)", 0, 50, 0, 5)

    with col2:
        loyer_stress = loyer_mensuel_cc * (1 - stress_loyer / 100) * (12 - stress_vacance)
        charges_stress = charges_totales_an * (1 + stress_charges / 100)
        impots_stress = max(0, df.iloc[0]["Impôts"]) * (1 + stress_impots / 100)
        cf_stress = (loyer_stress - (mensualite + assurance_emprunt_mensuel) * 12 - charges_stress - impots_stress) / 12

        css = "" if cf_stress >= 0 else "negative"
        metric_card("Cash-flow Stressé", f"{cf_stress:+,.0f} €/mois",
                     "Après application de tous les stress", css)

        rdt_stress = (loyer_stress / investissement_total) * 100
        metric_card("Rendement Stressé", f"{rdt_stress:.2f} %", "Rendement brut après stress",
                     "" if rdt_stress > taux_emprunt else "negative")

        if cf_stress < 0:
            mois_reserve = abs(cf_stress)
            reserve_2ans = mois_reserve * 24
            metric_card("Réserve nécessaire (2 ans)", f"{reserve_2ans:,.0f} €",
                         "Épargne de précaution recommandée", "negative")

    # Plan B concept
    st.markdown("### 📋 Check-list Plan B")
    strategy_box("Toujours avoir un Plan B (Chapitre B.3)", """
    <b>✓ Meublé tourisme</b> → Plan B en location classique à l'année<br>
    <b>✓ Colocation</b> → Plan B en location unique si réglementation change<br>
    <b>✓ Cosse Ancien</b> → Plan B en régime réel classique après expiration<br>
    <b>✓ LMNP</b> → Plan B en location nue si régime supprimé<br>
    <b>✓ Locataires CAF</b> → Plan B si réduction des aides au logement<br>
    <b>✓ Gros travaux</b> → Budget supplémentaire de 15-20% prévu
    """)

    # Seasonality
    st.markdown("### 📅 Saisonnalité du Marché Immobilier (Chapitre A.3)")
    mois = ["Jan", "Fév", "Mar", "Avr", "Mai", "Jun", "Jul", "Aoû", "Sep", "Oct", "Nov", "Déc"]
    variation = [-0.2, -0.2, -0.2, 1.8, 1.8, 1.8, -0.2, -0.2, -0.2, -1.4, -1.4, -1.4]
    colors_sais = ["#48bb78" if v < 0 else "#fc8181" for v in variation]

    fig_sais = go.Figure(go.Bar(
        x=mois, y=variation, marker_color=colors_sais,
        text=[f"{v:+.1f}%" for v in variation], textposition="outside",
    ))
    fig_sais.update_layout(
        title="Variation des prix selon la saison d'achat (vs moyenne annuelle)",
        yaxis_title="Variation (%)",
        **PLOTLY_LAYOUT,
    )
    fig_sais.add_annotation(x="Nov", y=-1.8, text="🏆 Meilleur moment<br>pour acheter",
                             showarrow=False, font=dict(color="#48bb78", size=11))
    fig_sais.add_annotation(x="Mai", y=2.2, text="⚠️ Pire moment<br>pour acheter",
                             showarrow=False, font=dict(color="#fc8181", size=11))
    st.plotly_chart(fig_sais, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        economies_saisonnieres = prix_achat * 0.032  # 3.2% spread
        metric_card("Économie potentielle (saisonnalité)",
                     f"{economies_saisonnieres:,.0f} €",
                     f"Acheter en Q4 vs Printemps (3.2% de {prix_achat:,.0f}€)")
    with col2:
        eco_majoree = economies_saisonnieres * 1.20  # +20% frais
        metric_card("Économie réelle (frais inclus)",
                     f"{eco_majoree:,.0f} €",
                     "Avec 20% de surcoûts (notaire, intérêts...)")


# ═══════════════════════════════════════════════════════════════
# TAB 7 — STRATÉGIES D'INVESTISSEMENT
# ═══════════════════════════════════════════════════════════════
with tabs[6]:
    st.markdown("## Stratégies d'Investissement (Chapitre E.2)")

    st.markdown("### 🗺️ Choix de la zone d'investissement")
    concept_box("Il n'y a pas UN marché, mais DES marchés immobiliers (Chapitre A.3)",
                "Depuis 2007 : Top 10 villes → forte hausse / Villes moyennes → stable / "
                "Zone rurale → baisse. Avec des taux bas et des prix stables en zone B2, "
                "le <b>différentiel rendement-taux</b> n'a jamais été aussi favorable !")

    # Zone comparison
    zones = pd.DataFrame({
        "Zone": ["A/ABis (Paris)", "B1 (Métropoles)", "B2 (Villes moyennes)", "C (Rural)"],
        "Rendement Brut Typique": [3, 5, 7.5, 12],
        "Risque Vacance": [5, 15, 25, 45],
        "Prix m² Moyen": [10000, 3500, 1800, 800],
        "Sérénité": [80, 70, 65, 40],
        "Cash-flow Possible": ["Très difficile", "Difficile", "Oui avec optimisation", "Oui, très positif"],
    })

    fig_zones = go.Figure()
    fig_zones.add_trace(go.Bar(
        name="Rendement Brut (%)", x=zones["Zone"], y=zones["Rendement Brut Typique"],
        marker_color="#48bb78", text=[f"{v}%" for v in zones["Rendement Brut Typique"]],
        textposition="outside",
    ))
    fig_zones.add_trace(go.Bar(
        name="Risque Vacance (%)", x=zones["Zone"], y=zones["Risque Vacance"],
        marker_color="#fc8181", text=[f"{v}%" for v in zones["Risque Vacance"]],
        textposition="outside",
    ))
    fig_zones.update_layout(
        title="Rendement vs Risque par zone géographique",
        barmode="group",
        yaxis_title="%",
        **PLOTLY_LAYOUT,
    )
    st.plotly_chart(fig_zones, use_container_width=True)

    strategy_box("Zone B2 = Sweet Spot (Chapitre C.1)",
                 "Meilleur compromis : prix raisonnables → rendements menant au cash-flow positif "
                 "+ taux de sérénité correct + demande locative présente. "
                 "Privilégiez <b>une ville proche de chez vous</b> pour la connaissance terrain.")

    # Strategy comparison table
    st.markdown("### 📋 Comparaison des stratégies")

    strategies = pd.DataFrame({
        "Stratégie": [
            "T1/T2 avec travaux (Agglo)",
            "Immeuble rapport (Rural)",
            "Pinel Maître d'Ouvrage",
            "T2-T3 Cosse Ancien (B2)",
            "Colocation (Grande surface)",
            "Meublé tourisme (Saisonnier)",
        ],
        "Rendement Visé": ["8-10%", "12-15%", "6-8%", "7-9%", "10-12%", "12-18%"],
        "Effort": ["⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
        "Sérénité": ["⭐⭐⭐", "⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐", "⭐"],
        "Fiscalité": ["LMNP Réel", "Cosse/Déficit F.", "Réduction Pinel", "Cosse + Déf.F.", "LMNP Réel", "LMNP/Micro-BIC"],
        "Profil Idéal": [
            "Cadre, peu de temps",
            "Gestionnaire actif, petits revenus",
            "Bricoleur, suivi chantier",
            "Prudent, patrimoine à long terme",
            "Social, gestion active",
            "Disponible, zone touristique",
        ]
    })
    st.dataframe(strategies, use_container_width=True, hide_index=True)

    # Proximity advantage
    st.markdown("### 🏠 L'avantage de la proximité")
    strategy_box("Investir près de chez soi = avantage ÉNORME (Chapitre C.1)", """
    <b>→ Connaissance terrain</b> : vous savez estimer le vrai prix, connaissez les quartiers, les rues à éviter<br>
    <b>→ Réactivité</b> : visiter dans la journée, décider vite sur une bonne affaire<br>
    <b>→ Réseau</b> : agents immobiliers, artisans, commerçants qui vous préviennent en premier<br>
    <b>→ Gestion</b> : mise en location directe, meilleur contrôle des locataires
    """)


# ═══════════════════════════════════════════════════════════════
# TAB 8 — OUTILS DCF & COMPARABLES
# ═══════════════════════════════════════════════════════════════
with tabs[7]:
    st.markdown("## Outils d'Analyse (Chapitres A.3, D.1, D.3)")

    st.markdown("### 📐 Valorisation DCF (Discount Cash-Flow)")
    concept_box("Valeur actuelle = Revenu Annuel / Taux d'actualisation",
                "Formule simplifiée pour des cash-flows perpétuels. Le taux d'actualisation = "
                "Taux sans risque + Prime de risque marché + Prime de risque spécifique. "
                "Utile pour valoriser des différences récurrentes (taxes foncières, garages, etc.)")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Valoriser une différence récurrente")
        flux_annuel = st.number_input("Flux annuel récurrent (€)", -5_000, 50_000, 500, step=50,
                                       help="Ex: différence de taxe foncière, loyer d'un garage...")
        taux_actualisation = st.slider("Taux d'actualisation (%)", 3.0, 15.0, 8.0, 0.5,
                                        help="≈ rendement que vous visez")

    with col2:
        valeur_dcf = flux_annuel / (taux_actualisation / 100)
        metric_card("Valeur Actuelle (DCF)", f"{valeur_dcf:,.0f} €",
                     f"Flux de {flux_annuel:,.0f}€/an actualisé à {taux_actualisation}%", "neutral")

        st.markdown("**Exemples du livre :**")
        st.markdown(f"- Différence taxe foncière 500€/an → vaut **{500/(taux_actualisation/100):,.0f}€**")
        st.markdown(f"- Garage louable 60€/mois → vaut **{720/(taux_actualisation/100):,.0f}€**")

    st.markdown("---")

    # Comparables method
    st.markdown("### 🔍 Méthode des Comparables (Prix au m²)")
    col1, col2 = st.columns(2)
    with col1:
        prix_m2_marche = st.number_input("Prix moyen au m² (quartier) (€)", 100, 20_000, 2_000, step=50)
        prix_m2_bien = prix_achat / surface_m2 if surface_m2 > 0 else 0
        decote_pct = ((prix_m2_marche - prix_m2_bien) / prix_m2_marche) * 100 if prix_m2_marche > 0 else 0

    with col2:
        metric_card("Prix au m² du bien", f"{prix_m2_bien:,.0f} €/m²",
                     f"Prix: {prix_achat:,.0f}€ / Surface: {surface_m2}m²", "neutral")
        css = "" if decote_pct > 0 else "negative"
        metric_card("Décote vs marché", f"{decote_pct:+.1f} %",
                     f"Marché: {prix_m2_marche:,.0f}€/m² → Marge de sécurité" if decote_pct > 0
                     else f"Surcote ! Marché: {prix_m2_marche:,.0f}€/m²", css)

    st.markdown("---")

    # Negotiation calculator
    st.markdown("### 🤝 Calculateur de Négociation (Chapitre D.3)")
    concept_box("Raisonner en « équivalent salaire »",
                "Si vous gagnez 2 000€/mois et épargnez 500€/mois, "
                "négocier 8 000€ = <b>16 mois d'épargne</b> gagnés en quelques minutes !")

    col1, col2 = st.columns(2)
    with col1:
        prix_affiche = st.number_input("Prix affiché (€)", 10_000, 2_000_000, 120_000, step=5_000)
        rabais_vise = st.slider("Rabais visé (%)", 0, 30, 10)

    with col2:
        prix_negocie = prix_affiche * (1 - rabais_vise / 100)
        economie = prix_affiche - prix_negocie
        if salaire_net > 0:
            equiv_mois = economie / salaire_net
            epargne_mensuelle = salaire_net * 0.20
            equiv_epargne = economie / epargne_mensuelle if epargne_mensuelle > 0 else 0
        else:
            equiv_mois = 0
            equiv_epargne = 0

        metric_card("Prix négocié", f"{prix_negocie:,.0f} €", f"Rabais de {rabais_vise}%")
        metric_card("Économie", f"{economie:,.0f} €",
                     f"≈ {equiv_mois:.0f} mois de salaire · {equiv_epargne:.0f} mois d'épargne")

    # DPE impact
    st.markdown("### 🌡️ Impact du DPE sur les prix (Chapitre A.2)")
    dpe_data = pd.DataFrame({
        "DPE": ["A-B", "C", "D (médiane)", "E", "F", "G"],
        "Maison (%)": [+10, +5, 0, -5, -10, -18],
        "Appartement (%)": [+3, +2, 0, -2, -6, -12],
    })

    fig_dpe = go.Figure()
    fig_dpe.add_trace(go.Bar(name="Maison", x=dpe_data["DPE"], y=dpe_data["Maison (%)"],
                              marker_color="#48bb78"))
    fig_dpe.add_trace(go.Bar(name="Appartement", x=dpe_data["DPE"], y=dpe_data["Appartement (%)"],
                              marker_color="#63b3ed"))
    fig_dpe.update_layout(
        title="Variation de prix par rapport au DPE médian (D)",
        barmode="group", yaxis_title="Variation (%)",
        **PLOTLY_LAYOUT,
    )
    fig_dpe.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.3)")
    st.plotly_chart(fig_dpe, use_container_width=True)

    # Floor impact
    st.markdown("### 🏢 Impact de l'Étage (sans ascenseur)")
    etages = pd.DataFrame({
        "Étage": ["RDC", "1er", "2ème ⭐", "3ème", "4ème", "5ème+"],
        "Décote/Surcote (%)": [-15, 0, +3, +2, -2, -8],
    })
    fig_etage = go.Figure(go.Bar(
        x=etages["Étage"], y=etages["Décote/Surcote (%)"],
        marker_color=["#fc8181", "#63b3ed", "#48bb78", "#48bb78", "#f6ad55", "#fc8181"],
        text=[f"{v:+d}%" for v in etages["Décote/Surcote (%)"]],
        textposition="outside",
    ))
    fig_etage.update_layout(
        title="Décote/Surcote par étage (sans ascenseur)",
        yaxis_title="%",
        **PLOTLY_LAYOUT,
    )
    fig_etage.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.3)")
    fig_etage.add_annotation(x="2ème ⭐", y=5, text="Idéal : 2ème sur cour",
                              showarrow=False, font=dict(color="#48bb78"))
    st.plotly_chart(fig_etage, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#718096; padding: 1rem 0; font-size: 0.85rem;">
    Les calculs sont des approximations à but pédagogique — consultez un professionnel pour vos investissements.
</div>
""", unsafe_allow_html=True)
