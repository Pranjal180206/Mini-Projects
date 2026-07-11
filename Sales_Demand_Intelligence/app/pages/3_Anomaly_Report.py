"""
Page 3 — Anomaly Report
Isolation Forest + Z-Score detected anomalies with explanation table.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.data_loader import load_weekly_sales, load_anomalies
from utils.model_utils import compute_anomalies

st.set_page_config(page_title="Anomaly Report", page_icon=None, layout="wide")

from utils.navigation import render_top_nav
render_top_nav()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif!important;}
.stApp{background:linear-gradient(135deg,#FDF8F8 0%,#FEF5F5 100%);}
[data-testid="stSidebar"]{background:#FFFFFF;border-right:1px solid rgba(0,0,0,0.05);}
[data-testid="stMetric"]{background:#FFFFFF;border:1px solid rgba(0,0,0,0.05);box-shadow:0 4px 6px -1px rgba(0,0,0,0.02);border-radius:12px;padding:16px 20px;}
[data-testid="stMetricValue"]{color:#C5B3D3!important;font-size:1.8rem!important;font-weight:700!important;}
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(0,0,0,0.05);
}
h1, h2, h3, h4, h5, h6 {color:#4A4A4A!important;}
p, .stMarkdown {color:#6B7280;}
hr {border-color: rgba(0,0,0,0.05) !important;}
</style>""", unsafe_allow_html=True)

PLOTLY_TEMPLATE = dict(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.4)',
    font=dict(color='#334155', family='Inter'),
    xaxis=dict(gridcolor='rgba(0,0,0,0.05)', linecolor='rgba(0,0,0,0.1)', title_font=dict(color='#475569')),
    yaxis=dict(gridcolor='rgba(0,0,0,0.05)', linecolor='rgba(0,0,0,0.1)', title_font=dict(color='#475569')),
)

st.markdown("""
<h1 style='background:linear-gradient(135deg,#C5B3D3,#F5CBCB);-webkit-background-clip:text;
           -webkit-text-fill-color:transparent;font-size:2.2rem;font-weight:800;margin-bottom:4px;'>
Anomaly Detection Report
</h1>
<p style='color:#6B7280;margin-top:0;'>AI-powered detection of unusual sales weeks using Isolation Forest &amp; Z-Score</p>
<hr style='border-color:rgba(0,0,0,0.05);'>
""", unsafe_allow_html=True)

# ── Settings ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Detection Settings")
    contamination = st.slider("Isolation Forest Contamination", 0.03, 0.15, 0.05, 0.01,
                               help="Expected fraction of anomalies in the data")
    z_threshold = st.slider("Z-Score Threshold (σ)", 1.5, 3.5, 2.0, 0.25,
                             help="Standard deviations from rolling mean to flag as anomaly")
    view_mode = st.radio("View Mode", ["Both Methods", "Isolation Forest Only", "Z-Score Only"])

# ── Load & compute ────────────────────────────────────────────────────────────
try:
    weekly_raw = load_weekly_sales()
except FileNotFoundError:
    st.error("Weekly sales data not found. Run the notebook first.")
    st.stop()

@st.cache_data
def run_anomaly_detection(cont, zt):
    from sklearn.ensemble import IsolationForest
    w = weekly_raw[weekly_raw['y'] > 0].copy().reset_index(drop=True)
    iso = IsolationForest(n_estimators=200, contamination=cont, random_state=42)
    w['iso_score']   = iso.fit_predict(w[['y']])
    w['iso_anomaly'] = w['iso_score'] == -1
    roll_mean = w['y'].rolling(window=8, min_periods=4, center=True).mean()
    roll_std  = w['y'].rolling(window=8, min_periods=4, center=True).std()
    w['z_score']    = (w['y'] - roll_mean) / roll_std
    w['z_anomaly']  = w['z_score'].abs() > zt
    w['roll_mean']  = roll_mean
    w['roll_upper'] = roll_mean + zt * roll_std
    w['roll_lower'] = roll_mean - zt * roll_std
    return w

weekly = run_anomaly_detection(contamination, z_threshold)
iso_count = weekly['iso_anomaly'].sum()
z_count   = weekly['z_anomaly'].sum()
both_count = (weekly['iso_anomaly'] & weekly['z_anomaly']).sum()

# ── KPIs ──────────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("Isolation Forest", f"{iso_count} anomalies", f"{iso_count/len(weekly)*100:.1f}% of weeks")
k2.metric("Z-Score",          f"{z_count} anomalies",  f"{z_count/len(weekly)*100:.1f}% of weeks")
k3.metric("Confirmed (Both)", f"{both_count} anomalies", "High confidence")
k4.metric("Total Weeks",      f"{len(weekly)}", "In dataset")

st.markdown("---")

# ── Plot: Isolation Forest ────────────────────────────────────────────────────
if view_mode in ["Both Methods", "Isolation Forest Only"]:
    st.markdown("#### Isolation Forest — Anomaly Detection")
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=weekly['ds'], y=weekly['y'],
        mode='lines', name='Weekly Sales',
        line=dict(color='#C5B3D3', width=1.8),
        hovertemplate='%{x|%d %b %Y}<br>$%{y:,.0f}'
    ))
    iso_mask = weekly['iso_anomaly']
    fig1.add_trace(go.Scatter(
        x=weekly.loc[iso_mask, 'ds'], y=weekly.loc[iso_mask, 'y'],
        mode='markers', name='Anomaly',
        marker=dict(color='#F5CBCB', size=12, symbol='circle',
                    line=dict(width=2, color='white')),
        hovertemplate='ANOMALY DETECTED<br>%{x|%d %b %Y}<br>Sales: $%{y:,.0f}'
    ))
    fig1.update_layout(**PLOTLY_TEMPLATE, height=360, hovermode='x unified',
                       legend=dict(orientation='h', yanchor='bottom', y=1.02))
    fig1.update_yaxes(tickprefix='$', tickformat='.2s')
    st.plotly_chart(fig1, use_container_width=True)

# ── Plot: Z-Score ─────────────────────────────────────────────────────────────
if view_mode in ["Both Methods", "Z-Score Only"]:
    st.markdown(f"#### Z-Score Detection — Rolling ±{z_threshold}σ Band")
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=pd.concat([weekly['ds'], weekly['ds'][::-1]]),
        y=pd.concat([weekly['roll_upper'], weekly['roll_lower'][::-1]]),
        fill='toself', fillcolor='rgba(197,179,211,0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        name=f'±{z_threshold}σ Band'
    ))
    fig2.add_trace(go.Scatter(
        x=weekly['ds'], y=weekly['roll_mean'],
        mode='lines', name='Rolling Mean',
        line=dict(color='rgba(0,0,0,0.4)', width=1, dash='dash'),
        hovertemplate='%{x|%d %b %Y}<br>MA: $%{y:,.0f}'
    ))
    fig2.add_trace(go.Scatter(
        x=weekly['ds'], y=weekly['y'],
        mode='lines', name='Weekly Sales',
        line=dict(color='#F5CBCB', width=2),
        hovertemplate='%{x|%d %b %Y}<br>$%{y:,.0f}'
    ))
    z_mask = weekly['z_anomaly']
    fig2.add_trace(go.Scatter(
        x=weekly.loc[z_mask, 'ds'], y=weekly.loc[z_mask, 'y'],
        mode='markers', name='Z-Score Anomaly',
        marker=dict(color='#DAB6C4', size=12, symbol='triangle-up',
                    line=dict(width=2, color='white')),
        hovertemplate='ANOMALY<br>%{x|%d %b %Y}<br>$%{y:,.0f}'
    ))
    fig2.update_layout(**PLOTLY_TEMPLATE, height=360, hovermode='x unified',
                       legend=dict(orientation='h', yanchor='bottom', y=1.02))
    fig2.update_yaxes(tickprefix='$', tickformat='.2s')
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ── Anomaly Table ─────────────────────────────────────────────────────────────
st.markdown("#### Detected Anomaly Events")
anomaly_rows = weekly[weekly['iso_anomaly'] | weekly['z_anomaly']].copy()
anomaly_rows['Date']       = pd.to_datetime(anomaly_rows['ds']).dt.strftime('%d %b %Y')
anomaly_rows['Sales ($)']  = anomaly_rows['y'].apply(lambda x: f"${x:,.0f}")
anomaly_rows['Detected By'] = anomaly_rows.apply(
    lambda r: 'Both' if r['iso_anomaly'] and r['z_anomaly']
              else ('Isolation Forest' if r['iso_anomaly'] else 'Z-Score'), axis=1)
anomaly_rows['Z-Score'] = anomaly_rows['z_score'].apply(
    lambda z: f"{z:+.2f}σ" if pd.notna(z) else 'N/A')

def get_cause(row):
    m = pd.to_datetime(row['ds']).month
    v = row['y']
    avg = weekly['y'].mean()
    if v > avg * 1.5:
        if m in [11, 12]: return 'Holiday season — Black Friday / Christmas surge'
        elif m in [8, 9]: return 'Back-to-school demand spike'
        elif m in [3, 4]: return 'Spring promotion / corporate Q1 purchasing'
        else:             return 'Bulk order or marketing campaign'
    else:
        if m in [1, 2]:   return 'Post-holiday spending lull'
        elif m in [6, 7]: return 'Summer slowdown'
        else:             return 'Possible supply disruption or data gap'

anomaly_rows['Likely Cause'] = anomaly_rows.apply(get_cause, axis=1)

display = anomaly_rows[['Date', 'Sales ($)', 'Detected By', 'Z-Score', 'Likely Cause']].reset_index(drop=True)
st.dataframe(display, use_container_width=True, hide_index=True)

# ── Method Comparison ─────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("#### Method Comparison")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    **Isolation Forest** (Density-based, Global)
    - Detects points that are statistically isolated from the data distribution
    - Works well for absolute outliers regardless of time context
    - Does not need a rolling window — learns the global data shape
    - Best for: detecting extreme one-off events
    """)
with col2:
    st.markdown(f"""
    **Z-Score** (Statistical, Context-aware)
    - Flags weeks that deviate more than {z_threshold}σ from their local rolling mean
    - Context-sensitive — respects seasonal patterns
    - May miss slow-moving anomalies that shift the baseline
    - Best for: detecting seasonally-unexpected deviations
    """)

agreement_pct = both_count / max(iso_count, z_count) * 100 if max(iso_count, z_count) > 0 else 0
st.info(f"**Agreement Rate**: Both methods agree on **{both_count}** out of **{max(iso_count, z_count)}** total flagged events ({agreement_pct:.0f}%). "
        f"High agreement indicates high-confidence anomalies worth investigating.")
