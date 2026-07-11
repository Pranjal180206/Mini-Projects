"""
model_utils.py — Lightweight forecasting helpers for Streamlit dashboard.
"""
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')


def get_season(month: int) -> str:
    if month in [12, 1, 2]:  return 'Winter'
    elif month in [3, 4, 5]: return 'Spring'
    elif month in [6, 7, 8]: return 'Summer'
    else:                    return 'Fall'


def create_lag_features(series_df: pd.DataFrame, lags=[1, 2, 3], window=3):
    """Create lag features for XGBoost time series."""
    from sklearn.preprocessing import LabelEncoder
    data = series_df.copy()
    data['Year']    = data['ds'].dt.year
    data['Month']   = data['ds'].dt.month
    data['Quarter'] = data['ds'].dt.quarter
    data['Season']  = data['Month'].apply(get_season)
    le = LabelEncoder()
    data['Season_enc'] = le.fit_transform(data['Season'])
    for lag in lags:
        data[f'lag_{lag}'] = data['y'].shift(lag)
    data[f'rolling_mean_{window}'] = data['y'].shift(1).rolling(window).mean()
    return data.dropna(), le


FEATURE_COLS = ['Year', 'Month', 'Quarter', 'Season_enc', 'lag_1', 'lag_2', 'lag_3', 'rolling_mean_3']


def xgb_forecast(monthly_df: pd.DataFrame, horizon: int = 3):
    """
    Train XGBoost on monthly_df and forecast `horizon` steps ahead.
    Returns: (forecast_dates, forecast_values, mae, rmse)
    """
    import xgboost as xgb
    from sklearn.metrics import mean_absolute_error, mean_squared_error

    ml_data, _ = create_lag_features(monthly_df)
    if len(ml_data) < horizon + 5:
        return [], [], None, None

    X = ml_data[FEATURE_COLS]
    y = ml_data['y']

    # Split: last `horizon` rows as test
    X_train, X_test = X.iloc[:-horizon], X.iloc[-horizon:]
    y_train, y_test = y.iloc[:-horizon], y.iloc[-horizon:]

    model = xgb.XGBRegressor(
        n_estimators=150, max_depth=3, learning_rate=0.05,
        subsample=0.8, colsample_bytree=0.8, random_state=42, verbosity=0
    )
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    mae  = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))

    forecast_dates = ml_data['ds'].tail(horizon).tolist()
    return forecast_dates, preds.tolist(), mae, rmse


def sarima_forecast(monthly_df: pd.DataFrame, horizon: int = 3):
    """
    Fit SARIMA(1,1,1)(1,1,1,12) and forecast `horizon` steps.
    Returns: (forecast_dates, forecast_values, lower_ci, upper_ci, mae, rmse)
    """
    try:
        from statsmodels.tsa.statespace.sarimax import SARIMAX
        from sklearn.metrics import mean_absolute_error, mean_squared_error

        ts = monthly_df.set_index('ds')['y']
        ts.index = pd.DatetimeIndex(ts.index, freq='MS')

        train = ts.iloc[:-horizon]
        test  = ts.iloc[-horizon:]

        model = SARIMAX(train, order=(1,1,1), seasonal_order=(1,1,1,12),
                        enforce_stationarity=False, enforce_invertibility=False)
        fit = model.fit(disp=False)

        fc = fit.get_forecast(steps=horizon)
        pred = fc.predicted_mean.values
        ci   = fc.conf_int(alpha=0.05)

        mae  = mean_absolute_error(test.values, pred)
        rmse = np.sqrt(mean_squared_error(test.values, pred))

        dates = list(test.index)
        return dates, pred.tolist(), ci.iloc[:, 0].tolist(), ci.iloc[:, 1].tolist(), mae, rmse
    except Exception as e:
        return [], [], [], [], None, None


def prophet_forecast(monthly_df: pd.DataFrame, horizon: int = 3):
    """
    Fit Prophet and forecast `horizon` steps ahead.
    Returns: (forecast_df, mae, rmse)
    """
    try:
        from prophet import Prophet
        from sklearn.metrics import mean_absolute_error, mean_squared_error

        train = monthly_df.iloc[:-horizon].copy()
        test  = monthly_df.iloc[-horizon:].copy()

        m = Prophet(yearly_seasonality=True, weekly_seasonality=False,
                    daily_seasonality=False, seasonality_mode='additive',
                    changepoint_prior_scale=0.05)
        m.fit(train)

        future = m.make_future_dataframe(periods=horizon, freq='MS')
        fc = m.predict(future)

        test_fc = fc[fc['ds'].isin(test['ds'])]
        if len(test_fc) == 0:
            test_fc = fc.tail(horizon)

        mae  = mean_absolute_error(test['y'].values, test_fc['yhat'].values[:horizon])
        rmse = np.sqrt(mean_squared_error(test['y'].values, test_fc['yhat'].values[:horizon]))

        return fc.tail(len(monthly_df) + horizon), mae, rmse
    except Exception as e:
        return pd.DataFrame(), None, None


def compute_anomalies(weekly_df: pd.DataFrame):
    """
    Run Isolation Forest + Z-Score anomaly detection on weekly sales.
    Returns weekly_df with anomaly columns added.
    """
    from sklearn.ensemble import IsolationForest

    w = weekly_df[weekly_df['y'] > 0].copy().reset_index(drop=True)

    iso = IsolationForest(n_estimators=200, contamination=0.05, random_state=42)
    w['iso_score']   = iso.fit_predict(w[['y']])
    w['iso_anomaly'] = w['iso_score'] == -1

    roll_mean = w['y'].rolling(window=8, min_periods=4, center=True).mean()
    roll_std  = w['y'].rolling(window=8, min_periods=4, center=True).std()
    w['z_score']   = (w['y'] - roll_mean) / roll_std
    w['z_anomaly'] = w['z_score'].abs() > 2.0
    w['roll_mean'] = roll_mean
    w['roll_upper'] = roll_mean + 2 * roll_std
    w['roll_lower'] = roll_mean - 2 * roll_std

    return w
