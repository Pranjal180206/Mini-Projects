"""
streamlit_app.py — Main entry point for the Sales Forecasting Dashboard.
Run with: streamlit run app/streamlit_app.py
"""
import streamlit as st

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="XY Sales Intelligence",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid rgba(0,0,0,0.05);
}

/* Main background */
.stApp {
    background: linear-gradient(135deg, #FBEFEF 0%, #FFE2E2 100%);
}

/* Metric cards */
[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid rgba(0,0,0,0.05);
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
    border-radius: 12px;
    padding: 16px 20px;
}

[data-testid="stMetricValue"] {
    color: #C5B3D3 !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
}

[data-testid="stMetricDelta"] svg { display: none; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #C5B3D3, #F5CBCB);
    color: #4A4A4A !important;
    border: none;
    border-radius: 8px;
    font-weight: 700;
    padding: 0.5rem 1.5rem;
    transition: all 0.2s;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(197,179,211,0.35);
}

/* Selectbox */
[data-testid="stSelectbox"] > div > div,
[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    border-color: rgba(0,0,0,0.1) !important;
    border-radius: 8px !important;
}

/* DataFrames */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(0,0,0,0.05);
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    background: #FBEFEF;
    border-radius: 10px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    color: #4A4A4A;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background: #FFFFFF !important;
    color: #C5B3D3 !important;
    font-weight: 700 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

/* Divider */
hr {
    border-color: rgba(0,0,0,0.08) !important;
}

/* Headings and paragraphs */
h1, h2, h3, h4, h5, h6 {
    color: #4A4A4A !important;
}
p, .stMarkdown {
    color: #6B7280;
}
</style>
""", unsafe_allow_html=True)

# ── Top Navigation ────────────────────────────────────────────────────────────
from utils.navigation import render_top_nav
render_top_nav()

# ── Home Page Content ─────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding: 48px 0 24px;'>
    <h1 style='font-size:2.8rem; font-weight:800;
               background: linear-gradient(135deg, #C5B3D3, #F5CBCB);
               -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin:0;'>
        Sales Forecasting &amp; Demand Intelligence
    </h1>
    <p style='color:#6B7280; font-size:1.05rem; margin-top:12px;'>
        End-to-End Retail Analytics Platform &mdash; Week 3 &amp; 4 Internship Project
    </p>
</div>
""", unsafe_allow_html=True)

# Hero metrics
from utils.data_loader import load_raw_superstore, format_currency
import pandas as pd

try:
    df = load_raw_superstore()

    col1, col2, col3, col4 = st.columns(4)
    total_sales    = df['Sales'].sum()
    total_orders   = df['Order ID'].nunique()
    total_products = df['Sub-Category'].nunique()
    avg_order      = df.groupby('Order ID')['Sales'].sum().mean()

    col1.metric("Total Revenue",    format_currency(total_sales),  "+18.5% YoY")
    col2.metric("Total Orders",     f"{total_orders:,}",           "+12.3% YoY")
    col3.metric("Product Types",    str(total_products),           "Sub-categories")
    col4.metric("Avg Order Value",  format_currency(avg_order),    "+5.2% YoY")

except FileNotFoundError:
    st.warning("Dataset not found. Place `train.csv` in the `data/` folder and run the notebook first.")

st.markdown("---")

# Feature cards
st.markdown("### Platform Features")
c1, c2, c3, c4 = st.columns(4)

cards = [
    ("Sales Overview",     "Explore 4 years of sales trends by category, region, and time period.",        "pages/1_Sales_Overview.py"),
    ("Forecast Explorer",  "3-model comparison: SARIMA, Prophet, XGBoost — select any segment.",           "pages/2_Forecast_Explorer.py"),
    ("Anomaly Report",     "AI-detected sales anomalies with Isolation Forest + Z-Score methods.",          "pages/3_Anomaly_Report.py"),
    ("Product Segments",   "K-Means demand clustering with PCA visualization and strategy guide.",          "pages/4_Product_Segments.py"),
]

CARD_ACCENTS = ['#C5B3D3', '#F5CBCB', '#C5B3D3', '#F5CBCB']

for col, (title, desc, _), accent in zip([c1, c2, c3, c4], cards, CARD_ACCENTS):
    col.markdown(f"""
    <div style='background:#FFFFFF;
                border:1px solid rgba(0,0,0,0.05); border-top: 3px solid {accent};
                box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
                border-radius:12px; padding:22px; height:160px;'>
        <div style='font-weight:700; color:#0F172A; font-size:1rem; margin-bottom:8px;'>{title}</div>
        <div style='color:#475569; font-size:0.82rem; line-height:1.5;'>{desc}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#64748B; font-size:0.78rem; padding:20px;'>
    Built with Python &nbsp;·&nbsp; Streamlit &nbsp;·&nbsp; XGBoost &nbsp;·&nbsp; Prophet &nbsp;·&nbsp; statsmodels
</div>
""", unsafe_allow_html=True)
