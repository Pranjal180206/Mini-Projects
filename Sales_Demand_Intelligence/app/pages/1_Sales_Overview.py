"""
Page 1 — Sales Overview Dashboard
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.data_loader import load_raw_superstore, format_currency

st.set_page_config(page_title="Sales Overview", page_icon=None, layout="wide")

from utils.navigation import render_top_nav
render_top_nav()

# ── Shared CSS ────────────────────────────────────────────────────────────────
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
    colorway=['#C5B3D3','#F5CBCB','#FFE2E2','#DAB6C4','#A692B8','#D69CA1']
)

COLORS = ['#C5B3D3','#F5CBCB','#FFE2E2','#DAB6C4','#A692B8','#D69CA1']

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<h1 style='background:linear-gradient(135deg,#C5B3D3,#F5CBCB);-webkit-background-clip:text;
           -webkit-text-fill-color:transparent;font-size:2.2rem;font-weight:800;margin-bottom:4px;'>
Sales Overview Dashboard
</h1>
<p style='color:#6B7280;margin-top:0;'>4-year retail performance analysis across categories, regions &amp; time</p>
<hr style='border-color:rgba(0,0,0,0.08);'>
""", unsafe_allow_html=True)

# ── Load Data ─────────────────────────────────────────────────────────────────
try:
    df = load_raw_superstore()
except FileNotFoundError:
    st.error("data/train.csv not found. Please run the notebook first.")
    st.stop()

# ── Sidebar Filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Filters")
    years = sorted(df['Year'].unique())
    sel_years = st.multiselect("Select Years", years, default=years, key="years_filter")
    categories = ['All'] + sorted(df['Category'].unique())
    sel_cat = st.selectbox("Category", categories, key="cat_filter")
    regions = ['All'] + sorted(df['Region'].unique())
    sel_region = st.selectbox("Region", regions, key="region_filter")

# Filter
filtered = df[df['Year'].isin(sel_years)]
if sel_cat != 'All':    filtered = filtered[filtered['Category'] == sel_cat]
if sel_region != 'All': filtered = filtered[filtered['Region']   == sel_region]

# ── KPI Row ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("Revenue",  format_currency(filtered['Sales'].sum()))
k2.metric("Orders",   f"{filtered['Order ID'].nunique():,}")
k3.metric("Customers", f"{filtered['Customer ID'].nunique():,}")
k4.metric("Avg Order", format_currency(filtered.groupby('Order ID')['Sales'].sum().mean()))

st.markdown("---")

# ── Chart Row 1 ───────────────────────────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    st.markdown("#### Total Sales by Year")
    yearly = filtered.groupby('Year')['Sales'].sum().reset_index()
    fig = px.bar(yearly, x='Year', y='Sales', color='Sales',
                 color_continuous_scale=['#FFE2E2', '#C5B3D3'],
                 labels={'Sales': 'Total Sales ($)'})
    fig.update_traces(marker_line_width=0, hovertemplate='%{x}<br>$%{y:,.0f}')
    fig.update_layout(**PLOTLY_TEMPLATE, showlegend=False,
                      coloraxis_showscale=False, height=350)
    fig.update_yaxes(tickprefix='$', tickformat='.2s')
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown("#### Revenue Share by Category")
    cat_rev = filtered.groupby('Category')['Sales'].sum().reset_index()
    fig2 = px.pie(cat_rev, values='Sales', names='Category',
                  color_discrete_sequence=COLORS,
                  hole=0.45)
    fig2.update_traces(textposition='inside', textinfo='percent+label',
                       hovertemplate='%{label}<br>$%{value:,.0f} (%{percent})',
                       marker=dict(line=dict(color='#FFFFFF', width=2)))
    fig2.update_layout(**PLOTLY_TEMPLATE, height=350,
                       legend=dict(orientation='h', yanchor='bottom', y=-0.2))
    st.plotly_chart(fig2, use_container_width=True)

# ── Monthly Trend ─────────────────────────────────────────────────────────────
st.markdown("#### Monthly Sales Trend")
monthly_trend = filtered.groupby(pd.Grouper(key='Order Date', freq='MS'))['Sales'].sum().reset_index()
fig3 = go.Figure()
fig3.add_trace(go.Scatter(
    x=monthly_trend['Order Date'], y=monthly_trend['Sales'],
    mode='lines', name='Monthly Sales',
    line=dict(color='#C5B3D3', width=2.5),
    fill='tozeroy', fillcolor='rgba(197,179,211,0.08)',
    hovertemplate='%{x|%b %Y}<br>$%{y:,.0f}'
))
# Add 3-month rolling average
roll = monthly_trend['Sales'].rolling(3, center=True).mean()
fig3.add_trace(go.Scatter(
    x=monthly_trend['Order Date'], y=roll,
    mode='lines', name='3-Month MA',
    line=dict(color='#F5CBCB', width=1.5, dash='dash'),
    hovertemplate='%{x|%b %Y}<br>MA: $%{y:,.0f}'
))
fig3.update_layout(**PLOTLY_TEMPLATE, height=380,
                   hovermode='x unified',
                   legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
fig3.update_yaxes(tickprefix='$', tickformat='.2s')
st.plotly_chart(fig3, use_container_width=True)

# ── Chart Row 2 ───────────────────────────────────────────────────────────────
c3, c4 = st.columns(2)

with c3:
    st.markdown("#### Sales by Region")
    region_sales = filtered.groupby('Region')['Sales'].sum().reset_index().sort_values('Sales', ascending=True)
    fig4 = px.bar(region_sales, x='Sales', y='Region', orientation='h',
                  color='Sales', color_continuous_scale=['#FFE2E2', '#C5B3D3'],
                  labels={'Sales': 'Total Sales ($)'})
    fig4.update_traces(marker_line_width=0, hovertemplate='%{y}<br>$%{x:,.0f}')
    fig4.update_layout(**PLOTLY_TEMPLATE, showlegend=False,
                       coloraxis_showscale=False, height=320)
    fig4.update_xaxes(tickprefix='$', tickformat='.2s')
    st.plotly_chart(fig4, use_container_width=True)

with c4:
    st.markdown("#### Sales by Ship Mode")
    ship_sales = filtered.groupby('Ship Mode')['Sales'].sum().reset_index().sort_values('Sales', ascending=False)
    fig5 = px.bar(ship_sales, x='Ship Mode', y='Sales',
                  color='Ship Mode', color_discrete_sequence=COLORS,
                  labels={'Sales': 'Total Sales ($)'})
    fig5.update_traces(marker_line_width=0, hovertemplate='%{x}<br>$%{y:,.0f}')
    fig5.update_layout(**PLOTLY_TEMPLATE, showlegend=False, height=320)
    fig5.update_yaxes(tickprefix='$', tickformat='.2s')
    st.plotly_chart(fig5, use_container_width=True)

# ── Sub-category Breakdown ────────────────────────────────────────────────────
st.markdown("#### Sub-Category Performance")
subcat = filtered.groupby(['Category', 'Sub-Category'])['Sales'].sum().reset_index().sort_values('Sales', ascending=False)
fig6 = px.treemap(subcat, path=['Category', 'Sub-Category'], values='Sales',
                  color='Sales', color_continuous_scale=['#FFE2E2', '#C5B3D3'],
                  hover_data={'Sales': ':.0f'})
fig6.update_layout(**PLOTLY_TEMPLATE, height=420)
fig6.update_traces(hovertemplate='<b>%{label}</b><br>Sales: $%{value:,.0f}')
st.plotly_chart(fig6, use_container_width=True)

# ── Data Table ────────────────────────────────────────────────────────────────
with st.expander("View Raw Data"):
    desired_cols = ['Order Date','Category','Sub-Category','Region','Segment','Sales','Quantity','Discount','Profit']
    available_cols = [c for c in desired_cols if c in filtered.columns]
    st.dataframe(
        filtered[available_cols]
        .sort_values('Order Date', ascending=False)
        .head(500)
        .reset_index(drop=True),
        use_container_width=True
    )
