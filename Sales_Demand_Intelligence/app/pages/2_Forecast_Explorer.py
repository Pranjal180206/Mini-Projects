"""
Page 2 — Forecast Explorer
Dropdown to select segment, slider for horizon, live forecast from best model.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.data_loader import load_raw_superstore, load_monthly_sales, format_currency
from utils.model_utils import xgb_forecast, sarima_forecast, prophet_forecast

st.set_page_config(page_title="Forecast Explorer", page_icon=None, layout="wide")

from utils.navigation import render_top_nav
render_top_nav()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif!important;}
.stApp{background:linear-gradient(135deg,#FBEFEF 0%,#FFE2E2 100%);}
[data-testid="stSidebar"]{background:#FFFFFF;border-right:1px solid rgba(0,0,0,0.05);}
[data-testid="stMetric"]{background:#FFFFFF;border:1px solid rgba(0,0,0,0.05);box-shadow:0 4px 6px -1px rgba(0,0,0,0.02);border-radius:12px;padding:16px 20px;}
[data-testid="stMetricValue"]{color:#C5B3D3!important;font-size:1.8rem!important;font-weight:700!important;}
.forecast-badge {
    display:inline-block; background:linear-gradient(135deg,#C5B3D3,#F5CBCB);
    color:#4A4A4A; border-radius:6px; padding:3px 10px; font-size:0.75rem; font-weight:600;
}
.stButton > button {
    background: linear-gradient(135deg, #C5B3D3, #F5CBCB) !important;
    color: #4A4A4A !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    padding: 0.5rem 1.5rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(197,179,211,0.35) !important;
}
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
Forecast Explorer
</h1>
<p style='color:#6B7280;margin-top:0;'>Compare 3 forecasting models across any category or region</p>
<hr style='border-color:rgba(0,0,0,0.05);'>
""", unsafe_allow_html=True)

# ── Controls ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Forecast Settings")
    segment_type = st.radio("Segment Type", ["Overall", "Category", "Region"], index=0, key="seg_type")

    try:
        df_raw = load_raw_superstore()
    except FileNotFoundError:
        st.error("Dataset not found.")
        st.stop()

    if segment_type == "Category":
        segment_name = st.selectbox("Select Category", sorted(df_raw['Category'].unique()), key="cat_sel")
    elif segment_type == "Region":
        segment_name = st.selectbox("Select Region", sorted(df_raw['Region'].unique()), key="reg_sel")
    else:
        segment_name = "All"

    horizon = st.slider("Forecast Horizon (months)", min_value=1, max_value=6, value=3, key="horizon_slider")
    model_choice = st.radio("Forecasting Model", ["XGBoost", "SARIMA", "Prophet"], index=0, key="model_sel")
    run_btn = st.button("Run Forecast", use_container_width=True)

# ── Load segment data ─────────────────────────────────────────────────────────
@st.cache_data
def get_segment_data(seg_type, seg_name):
    if seg_type == "Overall":
        return load_monthly_sales()
    filtered = df_raw[df_raw[seg_type] == seg_name] if seg_name != "All" else df_raw
    monthly = filtered.groupby(pd.Grouper(key='Order Date', freq='MS'))['Sales'].sum().reset_index()
    monthly.columns = ['ds', 'y']
    return monthly[monthly['y'] > 0].copy()

monthly_df = get_segment_data(segment_type, segment_name)

# ── Historical chart (always shown) ──────────────────────────────────────────
st.markdown(f"### Historical Sales — {segment_type}: **{segment_name}**")

fig_hist = go.Figure()
fig_hist.add_trace(go.Scatter(
    x=monthly_df['ds'], y=monthly_df['y'],
    mode='lines', name='Monthly Sales',
    line=dict(color='#C5B3D3', width=2),
    fill='tozeroy', fillcolor='rgba(197,179,211,0.07)',
    hovertemplate='%{x|%b %Y}<br>$%{y:,.0f}'
))
fig_hist.update_layout(**PLOTLY_TEMPLATE, height=300,
                        margin=dict(t=20, b=20))
fig_hist.update_yaxes(tickprefix='$', tickformat='.2s')
st.plotly_chart(fig_hist, use_container_width=True)

# ── Run Forecast ──────────────────────────────────────────────────────────────
if run_btn or True:  # Always show on load
    st.markdown(f"### {model_choice} Forecast — Next {horizon} Month(s)")

    with st.spinner(f"Running {model_choice} model..."):
        mae, rmse = None, None
        forecast_dates, forecast_vals = [], []
        lower_ci, upper_ci = [], []

        if model_choice == "XGBoost":
            forecast_dates, forecast_vals, mae, rmse = xgb_forecast(monthly_df, horizon)

        elif model_choice == "SARIMA":
            forecast_dates, forecast_vals, lower_ci, upper_ci, mae, rmse = sarima_forecast(monthly_df, horizon)

        elif model_choice == "Prophet":
            fc_df, mae, rmse = prophet_forecast(monthly_df, horizon)
            if not fc_df.empty:
                tail = fc_df.tail(horizon)
                forecast_dates = tail['ds'].tolist()
                forecast_vals  = tail['yhat'].tolist()
                lower_ci = tail['yhat_lower'].tolist()
                upper_ci = tail['yhat_upper'].tolist()

    if forecast_vals:
        # Metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("MAE",  format_currency(mae) if mae else "N/A", "Mean Abs Error")
        m2.metric("RMSE", format_currency(rmse) if rmse else "N/A", "Root Mean Sq Error")
        m3.metric("Avg Forecast", format_currency(np.mean(forecast_vals)))
        m4.metric("Peak Forecast", format_currency(max(forecast_vals)))

        st.markdown("---")

        # Forecast chart
        fig_fc = go.Figure()

        # Historical (last 18 months)
        hist_tail = monthly_df.tail(18)
        fig_fc.add_trace(go.Scatter(
            x=hist_tail['ds'], y=hist_tail['y'],
            mode='lines', name='Historical',
            line=dict(color='#C5B3D3', width=2.5),
            hovertemplate='%{x|%b %Y}<br>$%{y:,.0f}'
        ))

        # Confidence interval (if available)
        if lower_ci and upper_ci:
            fig_fc.add_trace(go.Scatter(
                x=list(forecast_dates) + list(reversed(forecast_dates)),
                y=list(upper_ci) + list(reversed(lower_ci)),
                fill='toself', fillcolor='rgba(245,203,203,0.3)',
                line=dict(color='rgba(255,255,255,0)'),
                name='95% Confidence Interval', showlegend=True
            ))

        # Forecast line
        fig_fc.add_trace(go.Scatter(
            x=forecast_dates, y=forecast_vals,
            mode='lines+markers', name=f'{model_choice} Forecast',
            line=dict(color='#F5CBCB', width=3, dash='dash'),
            marker=dict(size=10, color='#F5CBCB', symbol='diamond',
                        line=dict(width=2, color='white')),
            hovertemplate='%{x|%b %Y}<br>Forecast: $%{y:,.0f}'
        ))

        # Add vertical separator
        split_date = monthly_df['ds'].iloc[-1] if len(monthly_df) > 0 else None
        if split_date is not None:
            split_str = str(split_date)[:10]  # YYYY-MM-DD
            fig_fc.add_shape(type="line", x0=split_str, x1=split_str,
                             y0=0, y1=1, yref="paper",
                             line=dict(dash="dot", color="rgba(0,0,0,0.2)", width=1))
            fig_fc.add_annotation(x=split_str, y=1, yref="paper",
                                  text="Forecast Start", showarrow=False,
                                  font=dict(color="#64748B", size=11),
                                  xanchor="left", yanchor="bottom")

        fig_fc.update_layout(**PLOTLY_TEMPLATE, height=420, hovermode='x unified',
                              legend=dict(orientation='h', yanchor='bottom', y=1.02))
        fig_fc.update_yaxes(tickprefix='$', tickformat='.2s')
        st.plotly_chart(fig_fc, use_container_width=True)

        # Forecast table
        st.markdown("#### Forecast Values")
        has_ci = bool(lower_ci and upper_ci)
        fc_table = pd.DataFrame({
            'Date':             [pd.Timestamp(d).strftime('%B %Y') for d in forecast_dates],
            'Forecasted Sales': [format_currency(v) for v in forecast_vals],
            'Lower Bound':      [format_currency(v) for v in lower_ci] if has_ci else ['N/A'] * len(forecast_vals),
            'Upper Bound':      [format_currency(v) for v in upper_ci] if has_ci else ['N/A'] * len(forecast_vals),
        })
        st.dataframe(fc_table, use_container_width=True, hide_index=True)
        if not has_ci:
            st.caption("Confidence intervals are only available for SARIMA and Prophet models.")

    else:
        st.warning("Not enough data to generate a forecast for this segment. Try a different selection.")

# ── Model Info ────────────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("About the Models"):
    st.markdown("""
    | Model | Approach | Best For |
    |-------|----------|----------|
    | **XGBoost** | ML with lag features | Complex patterns, many segments |
    | **SARIMA** | Statistical ARIMA with seasonality | Classical time series, interpretability |
    | **Prophet** | Bayesian decomposition | Business calendars, holiday effects |
    """)
