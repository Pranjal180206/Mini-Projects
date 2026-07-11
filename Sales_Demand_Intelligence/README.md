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

## 🧠 Models Implemented

This project extensively relies on robust Machine Learning and Statistical models to extract insights:

### 1. Forecasting Models
- **XGBoost (Extreme Gradient Boosting)**: Used as the primary ML model. Extracts temporal features (month, quarter, day of week) to predict non-linear sales patterns. It achieved the best Mean Absolute Error (MAE) and Mean Absolute Percentage Error (MAPE).
- **Facebook Prophet**: An additive regression model that handles daily/weekly seasonality well and is robust to missing data and shifts in the trend.
- **SARIMA (Seasonal AutoRegressive Integrated Moving Average)**: A classical statistical model used as a baseline to capture exact seasonal periodicities in the time series.

### 2. Anomaly Detection Models
- **Isolation Forest**: An unsupervised machine learning algorithm that identifies anomalies by isolating outliers in the feature space (i.e., weeks with exceptionally high or low sales compared to the norm).
- **Z-Score Method**: A statistical rolling-band approach used as a secondary confirmation to flag data points falling outside 2 standard deviations.

### 3. Segmentation Models
- **K-Means Clustering**: Unsupervised learning used to group the 17 product sub-categories into 4 actionable business segments based on volume, volatility, and growth.
- **PCA (Principal Component Analysis)**: Dimensionality reduction technique to visualize the clustering segments in a clear 2D space.

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
