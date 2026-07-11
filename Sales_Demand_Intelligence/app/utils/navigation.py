import streamlit as st

def render_top_nav():
    st.markdown("""
    <style>
    /* Add some styling to make the top nav look nice and remove sidebar toggle if possible */
    [data-testid="collapsedControl"] { display: none; }
    </style>
    <div style='text-align:center; padding: 10px 0 10px;'>
        <div style='font-size:1.5rem; font-weight:800; color:#C5B3D3; letter-spacing:2px;'>XY SALES</div>
        <div style='font-size:0.7rem; color:#6B7280; letter-spacing:3px; margin-top:2px;'>INTELLIGENCE PLATFORM</div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(5)
    with cols[0]:
        st.page_link("streamlit_app.py", label="Home")
    with cols[1]:
        st.page_link("pages/1_Sales_Overview.py", label="Sales Overview")
    with cols[2]:
        st.page_link("pages/2_Forecast_Explorer.py", label="Forecast")
    with cols[3]:
        st.page_link("pages/3_Anomaly_Report.py", label="Anomalies")
    with cols[4]:
        st.page_link("pages/4_Product_Segments.py", label="Segments")
    
    st.markdown("<hr style='margin-top: 5px; margin-bottom: 20px; border-color:rgba(0,0,0,0.05);'>", unsafe_allow_html=True)
