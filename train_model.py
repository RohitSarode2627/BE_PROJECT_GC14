import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

print("Loading data.csv...")
df = pd.read_csv('data.csv')

# Parse timestamp in data.csv (format is DD-MM-YYYY HH:MM)
ts = pd.to_datetime(df['timestamp'], format='%d-%m-%Y %H:%M', errors='coerce')
if ts.isna().any():
    ts = ts.fillna(pd.to_datetime(df['timestamp'], errors='coerce'))

iso_week = ts.dt.isocalendar().week.astype(float)
dt_features = pd.DataFrame({
    'year': ts.dt.year.astype(float),
    'month': ts.dt.month.astype(float),
    'day': ts.dt.day.astype(float),
    'hour': ts.dt.hour.astype(float),
    'dayofyear': ts.dt.dayofyear.astype(float),
    'week': iso_week,
    'weekofyear': iso_week,
    'dayofweek': ts.dt.dayofweek.astype(float),
    'weekday': ts.dt.weekday.astype(float),
    'quarter': ts.dt.quarter.astype(float)
})

# Columns of data1:
# [0: year, 1: month, 2: day, 3: hour, 4: dayofyear, 5: week, 6: weekofyear,
#  7: dayofweek, 8: weekday, 9: quarter,
#  10: act379, 11: act13, 12: act279, 13: act323, 14: act363, 15: act302,
#  16: latitude, 17: longitude]
data1 = pd.concat([dt_features, df.drop('timestamp', axis=1)], axis=1)

X = data1.iloc[:, [1, 2, 3, 4, 6, 16, 17]].values
y = data1.iloc[:, [10, 11, 12, 13, 14, 15]].values

# Filter any NaN
valid_mask = ~np.isnan(X).any(axis=1) & ~np.isnan(y).any(axis=1)
X = X[valid_mask]
y = y[valid_mask]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=50)

print("Training RandomForestClassifier...")
rfc = RandomForestClassifier(n_estimators=100, random_state=42)
rfc.fit(X_train, y_train)

print(f"Train accuracy: {rfc.score(X_train, y_train):.4f}")
print(f"Test accuracy:  {rfc.score(X_test, y_test):.4f}")

os.makedirs('model', exist_ok=True)
joblib.dump(rfc, 'model/rf_model')
print("Model saved successfully to model/rf_model")
