# =========================================
# 🚀 IMPORTS
# =========================================
from fastapi import FastAPI
import joblib
import numpy as np
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
# =========================================
# ⚙️ INITIALIZE APP
# =========================================
app = FastAPI()


# =========================================
# 📦 LOAD TRAINED MODEL + COLUMNS
# =========================================
# model.pkl → trained ML model
# columns.pkl → ensures same feature order during prediction
model = joblib.load("model.pkl")
columns = joblib.load("columns.pkl")


# =========================================
# 🏠 ROOT ENDPOINT (HEALTH CHECK)
# =========================================
@app.get("/")
def home():
    return {"message": "Churn Prediction API is running"}


# =========================================
# 🔮 PREDICTION ENDPOINT
# =========================================
@app.post("/predict")
def predict(data: dict):
    try:
        df = pd.DataFrame([data])

        # ==============================
        # 🔹 BASIC CLEANING
        # ==============================
        df.drop(columns=['customerID'], errors='ignore', inplace=True)

        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
        df['TotalCharges'] = df['TotalCharges'].fillna(0)

        # ==============================
        # 🔹 FEATURE ENGINEERING
        # ==============================
        df['Charges_per_tenure'] = df['MonthlyCharges'] / (df['tenure'] + 1)
        df['TotalCharges_log'] = np.log1p(df['TotalCharges'])

        df['High_Spender'] = (df['MonthlyCharges'] > 70).astype(int)

        df['high_risk'] = (
            (df['MonthlyCharges'] > df['MonthlyCharges'].quantile(0.7)) &
            (df['tenure'] < df['tenure'].quantile(0.3))
        ).astype(int)

        df['tenure_group'] = pd.cut(
            df['tenure'],
            bins=[0,12,24,48,72],
            labels=[0,1,2,3],
            include_lowest=True
        ).astype(int)

        df['Contract_Risk'] = df['Contract'].map({
            'Month-to-month': 2,
            'One year': 1,
            'Two year': 0
        })

        service_cols = [
            'PhoneService','MultipleLines','OnlineSecurity','OnlineBackup',
            'DeviceProtection','TechSupport','StreamingTV','StreamingMovies'
        ]

        df['Total_Services'] = df[service_cols].apply(
            lambda x: x.isin(['Yes']).sum(), axis=1
        )

        # ==============================
        # 🔹 ENCODING (CRITICAL)
        # ==============================
        df = pd.get_dummies(df, drop_first=True)

        # ==============================
        # 🔹 ALIGN WITH TRAINING
        # ==============================
        df = df.reindex(columns=columns, fill_value=0)

        df = df.astype(float)

        # ==============================
        # 🔹 PREDICT
        # ==============================
        prediction = model.predict(df)[0]
        probability = model.predict_proba(df)[0][1]

        return {
            "prediction": int(prediction),
            "probability": float(probability)
        }

    except Exception as e:
        return {"error": str(e)}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)