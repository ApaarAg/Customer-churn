# =========================================
# 🚀 IMPORTS
# =========================================
from fastapi import FastAPI
import joblib
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
    
    # Convert incoming JSON to DataFrame
    df = pd.DataFrame([data])

    # Align columns with training data
    df = df.reindex(columns=columns, fill_value=0)

    # Model prediction
    prediction = model.predict(df)[0]

    # Probability of churn
    probability = model.predict_proba(df)[0][1]

    return {
        "prediction": int(prediction),
        "probability": float(probability)
    }



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)