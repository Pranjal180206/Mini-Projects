# 🛒 Sales Demand Intelligence Platform

An end-to-end sales forecasting and demand intelligence system designed to analyze historical retail data, forecast future sales, detect anomalies, and segment products based on demand patterns.

This platform provides actionable business intelligence using advanced time series modeling, machine learning, and interactive data visualization.

---

## 🌟 Key Features

1. **Sales Overview**
   - Explore 4 years of sales trends across categories, regions, and time periods.
   - Interactive visualizations for revenue breakdowns and growth analysis.

2. **Forecast Explorer**
   - **3-Model Comparison**: Evaluates and compares **SARIMA**, **Prophet**, and **XGBoost** models.
   - Dynamic segment selection (by Category or Region) with customizable forecast horizons.
   - Includes confidence intervals and error metrics (MAE, RMSE).

3. **Anomaly Detection**
   - Identifies unusual sales weeks using **Isolation Forest** (machine learning) and **Z-Score** (statistical rolling bands).
   - Explains likely causes for detected anomalies (e.g., holiday surges, supply chain disruptions).

4. **Product Demand Segmentation**
   - **K-Means Clustering** categorizes product demand patterns into strategic segments (e.g., "Growing Demand", "High Volatility", "Stable").
   - **PCA (Principal Component Analysis)** visualization for 2D cluster exploration.
   - Actionable stocking and inventory strategies for each segment.

---

## ⚙️ How It Works

The intelligence pipeline is broken down into two main phases: **Data Processing & Modeling**, and the **Interactive Dashboard**.

### 1. Data Pipeline & Modeling
- **Data Preprocessing**: Cleans raw transaction data, aggregates it into daily/weekly/monthly frequencies, and extracts time-based features.
- **Forecasting**: Fits multiple models to the historical data. Evaluates performance to recommend the best predictions.
- **Anomaly Detection**: Scans the weekly aggregated data to flag statistical outliers.
- **Clustering**: Extracts features like Sales Standard Deviation, Average Order Value, and YoY Growth per sub-category, then uses K-Means to identify distinct business strategies.
- *All models and processed datasets are cached locally for lightning-fast dashboard performance.*

### 2. Interactive Dashboard
- Built entirely on **Streamlit** with a custom, sleek top-navigation UI.
- Leverages **Plotly** for highly interactive, responsive charts.
- Provides immediate business recommendations based on backend ML inferences.

---

## 📁 Project Structure

```text
├── data/
│   ├── train.csv              ← Raw Superstore Sales data
│   └── vgsales.csv            ← Raw Video Game Sales data
├── notebooks/
│   └── sales_forecasting.ipynb ← Data exploration and model training
├── app/
│   ├── streamlit_app.py       ← Dashboard Main Entry
│   ├── pages/                 ← Sub-pages (Overview, Forecast, Anomalies, Segments)
│   └── utils/
│       ├── data_loader.py     ← Caching & data processing utilities
│       ├── model_utils.py     ← ML model inference functions
│       └── navigation.py      ← Custom UI navigation component
├── outputs/
│   ├── data/                  ← Processed datasets
│   ├── models/                ← Pickled model weights (.pkl)
│   └── plots/                 ← Exported static charts
├── .streamlit/
│   └── config.toml            ← Theme configuration
└── requirements.txt           ← Project dependencies
```

---

## 🚀 Quick Start

### 1. Setup Environment
Clone the repository and install the dependencies:
```bash
# Create a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

*(Note for Windows users: If you encounter issues installing `prophet`, try using `conda install -c conda-forge prophet` or install pystan first.)*

### 2. Run the Modeling Pipeline
Before running the dashboard, generate the required models and processed data:
```bash
cd notebooks
jupyter notebook sales_forecasting.ipynb
```
*Run all cells from top to bottom. This process will populate the `outputs/` folder.*

### 3. Launch the Dashboard
Start the Streamlit application:
```bash
streamlit run app/streamlit_app.py
```
Open your browser at **http://localhost:8501** to view the platform.

---

## 🛠️ Tech Stack

- **Data Processing**: `pandas`, `numpy`
- **Machine Learning & Time Series**: `scikit-learn` (Isolation Forest, K-Means, PCA), `xgboost`, `prophet`, `statsmodels` (SARIMA)
- **Frontend & Visualization**: `streamlit`, `plotly`
