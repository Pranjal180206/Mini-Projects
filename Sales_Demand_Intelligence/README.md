# 🛒 End-to-End Sales Forecasting & Demand Intelligence System
> **Internship Project — Week 3 & Week 4**  
> Superstore Sales Dataset (Kaggle) + Video Game Sales (Kaggle)

---

## 📁 Project Structure

```
Week 3-4/
├── data/
│   ├── train.csv              ← Superstore Sales (place here)
│   └── vgsales.csv            ← Video Game Sales (place here)
├── notebooks/
│   └── sales_forecasting.ipynb ← Main notebook (Tasks 1–6)
├── app/
│   ├── streamlit_app.py       ← Dashboard entry point
│   ├── pages/
│   │   ├── 1_Sales_Overview.py
│   │   ├── 2_Forecast_Explorer.py
│   │   ├── 3_Anomaly_Report.py
│   │   └── 4_Product_Segments.py
│   └── utils/
│       ├── data_loader.py
│       └── model_utils.py
├── outputs/
│   ├── data/                  ← Processed CSVs (auto-generated)
│   ├── models/                ← Saved model files (auto-generated)
│   └── plots/                 ← Exported charts (auto-generated)
├── report/
│   └── summary.md             ← Executive Business Report
├── requirements.txt
└── .streamlit/
    └── config.toml            ← Dark theme config
```

---

## 🚀 Quick Start

### Step 1: Place Datasets
Download from Kaggle and place in the `data/` folder:
- [Superstore Sales](https://www.kaggle.com/datasets/rohitsahoo/sales-forecasting) → `data/train.csv`
- [Video Game Sales](https://www.kaggle.com/datasets/gregorut/videogamesales) → `data/vgsales.csv`

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

> **Note on Prophet (Windows):** If Prophet install fails, try:
> ```bash
> conda install -c conda-forge prophet
> ```
> Or install separately: `pip install pystan==2.19.1.1 prophet`

### Step 3: Run the Jupyter Notebook (Tasks 1–6)
```bash
cd notebooks
jupyter notebook sales_forecasting.ipynb
```
Run all cells top-to-bottom. This will:
- Load and process data
- Run all 3 forecasting models (SARIMA, Prophet, XGBoost)
- Detect anomalies
- Perform clustering
- Save all model outputs to `outputs/`

### Step 4: Launch the Streamlit Dashboard (Task 7)
```bash
streamlit run app/streamlit_app.py
```
Open your browser at: **http://localhost:8501**

---

## 📋 Task Coverage

| Task | Description | Status |
|------|-------------|--------|
| Task 1 | Data Loading, Merging & EDA | ✅ Notebook Section 1 |
| Task 2 | Time Series Decomposition + ADF | ✅ Notebook Section 2 |
| Task 3 | SARIMA + Prophet + XGBoost | ✅ Notebook Section 3 |
| Task 4 | Segment-Level Forecasting | ✅ Notebook Section 4 |
| Task 5 | Anomaly Detection (IF + Z-Score) | ✅ Notebook Section 5 |
| Task 6 | K-Means Demand Clustering | ✅ Notebook Section 6 |
| Task 7 | Streamlit Dashboard (4 pages) | ✅ app/ |
| Task 8 | Executive Business Report | ✅ report/summary.md |

---

## ☁️ Deployment (Streamlit Community Cloud)

1. Push this entire project to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select repo → Set Main file: `app/streamlit_app.py`
5. Add your datasets as GitHub files OR use Streamlit Secrets for Kaggle API credentials
6. Click **Deploy** → Share your live link!

> **Important:** Kaggle datasets may need to be included in the repo (they are small enough). Alternatively, use `kaggle` Python package to download them on startup via `requirements.txt`.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| `pandas` | Data loading, manipulation |
| `statsmodels` | SARIMA, decomposition, ADF test |
| `prophet` | Facebook Prophet forecasting |
| `xgboost` | ML-based time series forecasting |
| `scikit-learn` | Isolation Forest, K-Means, PCA |
| `plotly` | Interactive charts |
| `streamlit` | Dashboard framework |
| `matplotlib/seaborn` | Notebook visualizations |

---

## 📧 Submission Checklist

- [ ] Notebook runs end-to-end without errors
- [ ] Model comparison table shows MAE, RMSE, MAPE for all 3 models
- [ ] Streamlit app runs locally on `localhost:8501`
- [ ] Streamlit app deployed and live link submitted
- [ ] `report/summary.md` converted to PDF/Word for submission
- [ ] All 4 Streamlit pages load and display charts correctly
