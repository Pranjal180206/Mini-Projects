"""
Page 4 — Product Demand Segments
K-Means clustering results with PCA scatter and sub-category membership table.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.data_loader import load_raw_superstore, load_demand_segments

st.set_page_config(page_title="Product Segments", page_icon=None, layout="wide")

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
Product Demand Segmentation
</h1>
<p style='color:#6B7280;margin-top:0;'>K-Means clustering to identify demand patterns across all product sub-categories</p>
<hr style='border-color:rgba(0,0,0,0.05);'>
""", unsafe_allow_html=True)

# ── Load or compute segments ──────────────────────────────────────────────────
@st.cache_data
def compute_segments():
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA

    try:
        df = load_raw_superstore()
    except FileNotFoundError:
        return pd.DataFrame()

    # Feature engineering
    subcat = df.groupby('Sub-Category').agg(
        Total_Sales   = ('Sales', 'sum'),
        Avg_Order_Val = ('Sales', 'mean'),
        Sales_Std     = ('Sales', 'std'),
        Order_Count   = ('Order ID', 'nunique'),
    ).reset_index()

    years = sorted(df['Year'].unique())
    if len(years) >= 2:
        yoy = df.groupby(['Sub-Category', 'Year'])['Sales'].sum().unstack(fill_value=0)
        yoy['Growth_Rate'] = (yoy[years[-1]] - yoy[years[-2]]) / yoy[years[-2]].replace(0, np.nan) * 100
        subcat = subcat.merge(yoy[['Growth_Rate']].reset_index(), on='Sub-Category', how='left')
    else:
        subcat['Growth_Rate'] = 0
    subcat['Growth_Rate'] = subcat['Growth_Rate'].fillna(0)

    feat_cols = ['Total_Sales', 'Avg_Order_Val', 'Sales_Std', 'Order_Count', 'Growth_Rate']
    X = subcat[feat_cols].fillna(0)
    scaler = StandardScaler()
    X_sc = scaler.fit_transform(X)

    km = KMeans(n_clusters=4, random_state=42, n_init=10)
    subcat['Cluster'] = km.fit_predict(X_sc)

    pca = PCA(n_components=2, random_state=42)
    X_pca = pca.fit_transform(X_sc)
    subcat['PC1'] = X_pca[:, 0]
    subcat['PC2'] = X_pca[:, 1]

    # Auto label
    centroids = subcat.groupby('Cluster')[feat_cols].mean()
    def label_c(c):
        gr = centroids.loc[c, 'Growth_Rate']
        st_ = centroids.loc[c, 'Sales_Std']
        ts = centroids.loc[c, 'Total_Sales']
        if gr > 20:    return 'Growing Demand'
        elif gr < -10: return 'Declining Demand'
        elif st_ > centroids['Sales_Std'].mean(): return 'High Volatility'
        elif ts > centroids['Total_Sales'].mean(): return 'High Volume, Stable'
        else:          return 'Low Volume, Stable'
    subcat['Cluster_Label'] = subcat['Cluster'].map({c: label_c(c) for c in range(4)})
    subcat['var_pct'] = f"{pca.explained_variance_ratio_[0]*100:.1f}% / {pca.explained_variance_ratio_[1]*100:.1f}%"
    return subcat

subcat_df = compute_segments()

if subcat_df.empty:
    st.error("Dataset not found. Please ensure `data/train.csv` is present and run the notebook.")
    st.stop()

# ── KPIs ──────────────────────────────────────────────────────────────────────
cluster_counts = subcat_df['Cluster_Label'].value_counts()
k1, k2, k3, k4 = st.columns(4)
k1.metric("Sub-categories", str(len(subcat_df)))
k2.metric("Clusters", "4")
k3.metric("Growing", str(sum('Growing' in l for l in subcat_df['Cluster_Label'])))
k4.metric("Declining", str(sum('Declining' in l for l in subcat_df['Cluster_Label'])))

st.markdown("---")

# ── Scatter Plot ──────────────────────────────────────────────────────────────
st.markdown("#### Demand Cluster Visualization (PCA 2D)")

CLUSTER_COLORS = {
    'Growing Demand':     '#C5B3D3',
    'Declining Demand':   '#F5CBCB',
    'High Volatility':    '#DAB6C4',
    'High Volume, Stable':'#A692B8',
    'Low Volume, Stable': '#D69CA1',
}

fig_scatter = px.scatter(
    subcat_df, x='PC1', y='PC2',
    color='Cluster_Label',
    text='Sub-Category',
    size='Total_Sales',
    size_max=40,
    color_discrete_map=CLUSTER_COLORS,
    hover_data={
        'PC1': False, 'PC2': False,
        'Total_Sales': ':$,.0f',
        'Avg_Order_Val': ':$,.0f',
        'Growth_Rate': ':.1f%',
        'Cluster_Label': True
    },
    labels={'Cluster_Label': 'Demand Segment'}
)
fig_scatter.update_traces(
    textposition='top center',
    textfont=dict(size=9, color='#334155'),
    marker=dict(line=dict(width=1.5, color='rgba(255,255,255,0.9)'))
)
fig_scatter.update_layout(
    **PLOTLY_TEMPLATE, height=520,
    xaxis_title="Principal Component 1 (Sales Volume axis)",
    yaxis_title="Principal Component 2 (Volatility axis)",
    legend=dict(title='Demand Segment', orientation='v', x=1.02, y=1)
)
st.plotly_chart(fig_scatter, use_container_width=True)

# ── Cluster Bars ──────────────────────────────────────────────────────────────
st.markdown("#### Revenue by Cluster")
cluster_rev = subcat_df.groupby('Cluster_Label')['Total_Sales'].sum().reset_index()
cluster_rev['color'] = cluster_rev['Cluster_Label'].map(CLUSTER_COLORS)
fig_bar = go.Figure(go.Bar(
    x=cluster_rev['Cluster_Label'], y=cluster_rev['Total_Sales'],
    marker_color=cluster_rev['color'], marker_line_width=0,
    hovertemplate='%{x}<br>$%{y:,.0f}'
))
fig_bar.update_layout(**PLOTLY_TEMPLATE, height=300, showlegend=False)
fig_bar.update_yaxes(tickprefix='$', tickformat='.2s')
st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# ── Membership Table ──────────────────────────────────────────────────────────
st.markdown("#### Sub-Category &rarr; Cluster Membership", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Filter")
    selected_cluster = st.multiselect(
        "Filter by Cluster",
        sorted(subcat_df['Cluster_Label'].unique()),
        default=list(subcat_df['Cluster_Label'].unique()),
        key="cluster_filter"
    )

filtered_df = subcat_df[subcat_df['Cluster_Label'].isin(selected_cluster)]
display_table = filtered_df[['Sub-Category', 'Cluster_Label', 'Total_Sales',
                              'Avg_Order_Val', 'Growth_Rate', 'Sales_Std']].copy()
display_table.columns = ['Sub-Category', 'Demand Cluster', 'Total Revenue ($)',
                          'Avg Order ($)', 'YoY Growth (%)', 'Sales Volatility ($)']
display_table['Total Revenue ($)']   = display_table['Total Revenue ($)'].apply(lambda x: f"${x:,.0f}")
display_table['Avg Order ($)']        = display_table['Avg Order ($)'].apply(lambda x: f"${x:,.0f}")
display_table['YoY Growth (%)']       = display_table['YoY Growth (%)'].apply(lambda x: f"{x:+.1f}%")
display_table['Sales Volatility ($)'] = display_table['Sales Volatility ($)'].apply(lambda x: f"${x:,.0f}")

st.dataframe(display_table.reset_index(drop=True), use_container_width=True, hide_index=True)

st.markdown("---")

# ── Stocking Strategy ─────────────────────────────────────────────────────────
st.markdown("#### Recommended Stocking Strategy per Cluster")

strategies = {
    "High Volume, Stable": {
        "color": "#A692B8",
        "strategy": "Maintain high safety stock. Use automated reorder points (ROP).",
        "action": "JIT restocking with minimum 4–6 week buffer. Prioritize shelf space.",
        "risk": "Low — predictable demand reduces stockout risk"
    },
    "Growing Demand": {
        "color": "#C5B3D3",
        "strategy": "Proactively increase stock levels QoQ. Negotiate better supplier terms now.",
        "action": "Increase order quantities 15–20% per quarter. Add secondary supplier.",
        "risk": "Medium — growth may plateau; avoid over-commitment to long purchase orders"
    },
    "High Volatility": {
        "color": "#DAB6C4",
        "strategy": "Keep 1.5–2x safety stock to absorb demand spikes.",
        "action": "Shorter supplier contracts, weekly stock review, flexible ordering.",
        "risk": "High — unpredictable weeks may cause stockouts or overstock"
    },
    "Declining Demand": {
        "color": "#F5CBCB",
        "strategy": "Reduce stock levels. Run clearance promotions. Do not reorder until <2 weeks supply.",
        "action": "Flag for product rationalization. Consider SKU discontinuation.",
        "risk": "High — holding cost grows as sales slow; mark down aggressively"
    },
    "Low Volume, Stable": {
        "color": "#D69CA1",
        "strategy": "Keep minimum inventory, order only to replace sold stock.",
        "action": "Slow-moving inventory review. Consider dropshipping if possible.",
        "risk": "Low — but capital is tied up in slow moving goods."
    }
}

for cluster_label, info in strategies.items():
    if cluster_label in subcat_df['Cluster_Label'].values:
        with st.expander(f"{cluster_label}", expanded=False):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(f"""
                <div style='background:rgba({','.join(str(int(info["color"].lstrip('#')[i:i+2],16)) for i in (0,2,4))},0.15);
                            border:1px solid {info["color"]}40; border-radius:10px; padding:16px; text-align:center;'>
                    <div style='color:{info["color"]}; font-weight:700; font-size:1.1rem; margin-bottom:8px;'>RISK LEVEL</div>
                    <div style='color:#334155; font-size:0.85rem;'>{info["risk"]}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"**Strategy:** {info['strategy']}")
                st.markdown(f"**Action:** {info['action']}")
                members = subcat_df[subcat_df['Cluster_Label'] == cluster_label]['Sub-Category'].tolist()
                st.markdown(f"**Products in this cluster:** {', '.join(members)}")
