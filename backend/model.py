# =========================================
# 🤖 MODELING & COMPARISON
# =========================================
import seaborn as sns
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score
)
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier

# =========================================
# 🔀 SPLIT
# =========================================
df=pd.read_csv(r"data\cleaned_data.csv")
X = df.drop(columns=['Churn'])
y = df['Churn']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# =========================================
# ⚖️ IMBALANCE HANDLING
# =========================================
scale_pos_weight = len(y_train[y_train==0]) / len(y_train[y_train==1])


# =========================================
# 🌲 RANDOM FOREST
# =========================================
rf = RandomForestClassifier(random_state=42)

rf_param = {
    'n_estimators': [100, 200],
    'max_depth': [5, 10, None],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2]
}

rf_grid = GridSearchCV(rf, rf_param, cv=3, scoring='f1', n_jobs=-1)
rf_grid.fit(X_train, y_train)

rf_best = rf_grid.best_estimator_


# =========================================
# ⚡ XGBOOST
# =========================================
xgb = XGBClassifier(
    eval_metric='logloss',
    random_state=42,
    scale_pos_weight=scale_pos_weight,
    tree_method='hist'
)

xgb_param = {
    'n_estimators': [100, 200],
    'max_depth': [5, 7, 9],
    'learning_rate': [0.03, 0.05],
    'subsample': [0.6, 0.8],
    'colsample_bytree': [0.6, 0.8]
}

xgb_grid = GridSearchCV(xgb, xgb_param, cv=3, scoring='f1', n_jobs=-1)
xgb_grid.fit(X_train, y_train)

xgb_best = xgb_grid.best_estimator_


# =========================================
# 📉 LOGISTIC REGRESSION (BASELINE)
# =========================================
lr = LogisticRegression(max_iter=1000)

lr_param = {
    'C': [0.1, 1, 10],
    'penalty': ['l2']
}

lr_grid = GridSearchCV(lr, lr_param, cv=3, scoring='f1', n_jobs=-1)
lr_grid.fit(X_train, y_train)

lr_best = lr_grid.best_estimator_


# =========================================
# 📊 MODEL COMPARISON
# =========================================
models = {
    "RandomForest": rf_best,
    "XGBoost": xgb_best,
    "LogisticRegression": lr_best
}

results = []

threshold = 0.48  # keep same for fair comparison

for name, model in models.items():
    y_prob = model.predict_proba(X_test)[:,1]
    y_pred = (y_prob > threshold).astype(int)

    results.append({
        "Model": name,
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred),
        "Recall": recall_score(y_test, y_pred),
        "F1": f1_score(y_test, y_pred),
        "ROC_AUC": roc_auc_score(y_test, y_prob)
    })

results_df = pd.DataFrame(results)
print("\nMODEL COMPARISON:\n", results_df)


# =========================================
# 📊 VISUAL COMPARISON
# =========================================
results_df.set_index("Model").plot(kind="bar", figsize=(10,6))
plt.title("Model Comparison")
plt.xticks(rotation=0)
plt.show()


# =========================================
# 🏆 BEST MODEL
# =========================================
best_model_name = results_df.sort_values(by="F1", ascending=False).iloc[0]["Model"]
print("\nBest Model based on F1:", best_model_name)
# =========================================
# 💾 SAVE BEST MODEL
# =========================================
best_model = models[best_model_name]

joblib.dump(best_model, "model.pkl")
joblib.dump(X.columns, "columns.pkl")

print("Model and columns saved successfully")