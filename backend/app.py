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
        # ==============================
        # 🔹 CREATE DF
        # ==============================
        df = pd.DataFrame([data])

        # ==============================
        # 🔹 MATCH TRAINING COLUMNS
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