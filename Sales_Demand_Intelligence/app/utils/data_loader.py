"""
data_loader.py — Shared data loading & preprocessing utilities for Streamlit dashboard.
All functions use @st.cache_data for performance.
"""
import pandas as pd
import numpy as np
import streamlit as st
from pathlib import Path

# ── Path setup ────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent.parent  # Week 3-4/
DATA_DIR   = ROOT / "outputs" / "data"
MODELS_DIR = ROOT / "outputs" / "models"
RAW_DIR    = ROOT / "data"


@st.cache_data
def load_raw_superstore() -> pd.DataFrame:
    """Load and preprocess the Superstore Sales dataset."""
    path = RAW_DIR / "train.csv"
    df = pd.read_csv(path, encoding='latin-1')
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='mixed', dayfirst=False)
    df['Ship Date']  = pd.to_datetime(df['Ship Date'],  format='mixed', dayfirst=False)
    df['Year']       = df['Order Date'].dt.year
    df['Month']      = df['Order Date'].dt.month
    df['Quarter']    = df['Order Date'].dt.quarter
    df['ShipDays']   = (df['Ship Date'] - df['Order Date']).dt.days

    def get_season(month):
        if month in [12, 1, 2]:  return 'Winter'
        elif month in [3, 4, 5]: return 'Spring'
        elif month in [6, 7, 8]: return 'Summer'
        else:                    return 'Fall'
    df['Season'] = df['Month'].apply(get_season)
    return df


@st.cache_data
def load_monthly_sales() -> pd.DataFrame:
    """Load processed monthly sales (ds, y columns)."""
    path = DATA_DIR / "monthly_sales.csv"
    if path.exists():
        return pd.read_csv(path, parse_dates=['ds'])
    # Fallback: compute on the fly
    df = load_raw_superstore()
    monthly = df.groupby(pd.Grouper(key='Order Date', freq='MS'))['Sales'].sum().reset_index()
    monthly.columns = ['ds', 'y']
    return monthly[monthly['y'] > 0].copy()


@st.cache_data
def load_weekly_sales() -> pd.DataFrame:
    """Load processed weekly sales."""
    path = DATA_DIR / "weekly_sales.csv"
    if path.exists():
        return pd.read_csv(path, parse_dates=['ds'])
    df = load_raw_superstore()
    weekly = df.groupby(pd.Grouper(key='Order Date', freq='W'))['Sales'].sum().reset_index()
    weekly.columns = ['ds', 'y']
    return weekly[weekly['y'] > 0].copy()


@st.cache_data
def load_anomalies() -> pd.DataFrame:
    """Load pre-computed anomaly data."""
    path = DATA_DIR / "anomalies.csv"
    if path.exists():
        return pd.read_csv(path, parse_dates=['ds'])
    return pd.DataFrame()


@st.cache_data
def load_demand_segments() -> pd.DataFrame:
    """Load product demand segmentation results."""
    path = DATA_DIR / "demand_segments.csv"
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()


@st.cache_data
def load_model_results() -> dict:
    """Load model comparison results."""
    import json
    path = DATA_DIR / "model_results.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


@st.cache_data
def get_segment_monthly(segment_type: str, segment_name: str) -> pd.DataFrame:
    """
    Get monthly sales for a given segment (category or region).
    segment_type: 'Category' or 'Region'
    segment_name: e.g. 'Technology', 'West'
    """
    df = load_raw_superstore()
    filtered = df[df[segment_type] == segment_name] if segment_name != 'All' else df
    monthly = filtered.groupby(pd.Grouper(key='Order Date', freq='MS'))['Sales'].sum().reset_index()
    monthly.columns = ['ds', 'y']
    return monthly[monthly['y'] > 0].copy()


def format_currency(value: float) -> str:
    if value >= 1_000_000:
        return f"${value/1_000_000:.2f}M"
    elif value >= 1_000:
        return f"${value/1_000:.1f}K"
    return f"${value:.0f}"
