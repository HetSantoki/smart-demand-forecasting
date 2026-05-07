import joblib
import pandas as pd
import numpy as np
from datetime import timedelta
import os

BASE_DIR = r"D:\Smart Demand Forecasting"

pipeline     = joblib.load(os.path.join(BASE_DIR, 'Models', 'demand_pipeline.pkl'))
feature_cols = joblib.load(os.path.join(BASE_DIR, 'Models', 'feature_cols.pkl'))

daily_demand = pd.read_csv(
    os.path.join(BASE_DIR, 'data', 'daily_demand.csv'),
    index_col='Date', parse_dates=True
)

df_clean = pd.read_csv(
    os.path.join(BASE_DIR, 'data', 'cleaned_transactions.csv'),
    parse_dates=['InvoiceDate']
)

# ── UK Festival dates in dataset range ─────────────────────
FESTIVALS = [
    {"date": "2010-12-25", "name": "Christmas 2010"},
    {"date": "2011-01-01", "name": "New Year 2011"},
    {"date": "2011-02-14", "name": "Valentine's Day"},
    {"date": "2011-04-24", "name": "Easter Sunday"},
    {"date": "2011-08-29", "name": "Summer Bank Holiday"},
    {"date": "2011-10-31", "name": "Halloween"},
    {"date": "2011-12-25", "name": "Christmas 2011"},
]

# ── Helper: build lag features for any daily series ────────
def build_features(series, next_date):
    lag1  = series.iloc[-1]
    lag7  = series.iloc[-7]  if len(series) >= 7  else series.mean()
    lag14 = series.iloc[-14] if len(series) >= 14 else series.mean()
    lag30 = series.iloc[-30] if len(series) >= 30 else series.mean()

    roll7  = series.iloc[-7:].mean()  if len(series) >= 7  else series.mean()
    roll14 = series.iloc[-14:].mean() if len(series) >= 14 else series.mean()
    roll30 = series.iloc[-30:].mean() if len(series) >= 30 else series.mean()

    return pd.DataFrame([{
        'Lag_1'     : lag1,  'Lag_7'     : lag7,
        'Lag_14'    : lag14, 'Lag_30'    : lag30,
        'Rolling_7' : roll7, 'Rolling_14': roll14,
        'Rolling_30': roll30,
        'DayOfWeek' : next_date.dayofweek,
        'Month'     : next_date.month,
        'Week'      : int(next_date.isocalendar()[1]),
        'IsWeekend' : int(next_date.dayofweek >= 5),
        'Quarter'   : next_date.quarter,
    }])

# ── Overall demand forecast ─────────────────────────────────
def predict_future(days=30):
    data      = daily_demand['TotalQuantity'].copy()
    last_date = data.index[-1]
    future_dates, future_quantities = [], []

    for i in range(1, days + 1):
        next_date = last_date + timedelta(days=i)
        row       = build_features(data, next_date)
        pred      = max(0, pipeline.predict(row[feature_cols])[0])
        future_dates.append(next_date.strftime('%Y-%m-%d'))
        future_quantities.append(round(pred))
        data.loc[next_date] = pred

    return future_dates, future_quantities

# ── Top products list ───────────────────────────────────────
def get_top_products(n=40):
    top = (
        df_clean.groupby('Description')['Quantity']
        .sum().sort_values(ascending=False).head(n)
    )
    return top.index.tolist()

# ── Product-wise forecast ───────────────────────────────────
def predict_product(product_name, days=30):
    prod_df = df_clean[df_clean['Description'] == product_name].copy()
    prod_df['Date'] = prod_df['InvoiceDate'].dt.date

    daily = prod_df.groupby('Date')['Quantity'].sum().reset_index()
    daily['Date'] = pd.to_datetime(daily['Date'])
    daily = daily.set_index('Date').sort_index()

    full_range = pd.date_range(start=daily.index.min(), end=daily.index.max(), freq='D')
    daily = daily.reindex(full_range, fill_value=0)

    # Historical — last 60 days
    hist_dates = daily.index[-60:].strftime('%Y-%m-%d').tolist()
    hist_qty   = daily['Quantity'].iloc[-60:].tolist()

    # Forecast
    series = daily['Quantity'].copy()
    last_date = series.index[-1]
    future_dates, future_qty = [], []

    for i in range(1, days + 1):
        next_date = last_date + timedelta(days=i)
        row       = build_features(series, next_date)
        pred      = max(0, pipeline.predict(row[feature_cols])[0])
        future_dates.append(next_date.strftime('%Y-%m-%d'))
        future_qty.append(round(pred))
        series.loc[next_date] = pred

    return hist_dates, hist_qty, future_dates, future_qty

# ── Stockout alert table ────────────────────────────────────
def get_stockout_alerts(n=15):
    top_products = get_top_products(n)
    alerts = []

    for prod in top_products:
        prod_df = df_clean[df_clean['Description'] == prod]
        daily   = prod_df.groupby(
            prod_df['InvoiceDate'].dt.date
        )['Quantity'].sum()

        if len(daily) < 14:
            continue

        avg_demand    = round(daily.mean())
        recent_demand = round(daily.iloc[-7:].mean())
        trend         = round(((recent_demand - avg_demand) / avg_demand) * 100, 1) if avg_demand > 0 else 0
        risk          = 'High' if recent_demand > avg_demand * 1.5 else \
                        'Medium' if recent_demand > avg_demand * 1.2 else 'Low'

        alerts.append({
            'product'       : prod[:40],
            'avg_demand'    : f"{avg_demand:,}",
            'recent_demand' : f"{recent_demand:,}",
            'trend'         : f"+{trend}%" if trend > 0 else f"{trend}%",
            'risk'          : risk,
        })

    alerts.sort(key=lambda x: x['risk'])
    return alerts