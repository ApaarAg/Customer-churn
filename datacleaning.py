# =========================================
# IMPORTS
# =========================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency



# =========================================
# 📥 LOAD DATA
# =========================================
df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")


# =========================================
# 🔍 BASIC EDA
# =========================================
print("Shape:", df.shape)
print("\nColumns:", df.columns)
print("\nInfo:")
df.info()
print("\nMissing Values:\n", df.isna().sum())

df_dup = df.copy()


# =========================================
# 📊 CATEGORICAL EDA (PRESERVED)
# =========================================
cat_cols = df.select_dtypes(include=['object']).columns

# for col in cat_cols:
#     plt.figure(figsize=(6,4))
#     sns.countplot(x=col, hue='Churn', data=df_dup)
#     plt.title(f"{col} vs Churn")
#     plt.xticks(rotation=45)
#     plt.tight_layout()
#     plt.show()

# for col in cat_cols:
#     cr = pd.crosstab(df_dup[col], df_dup['Churn'], normalize='index') * 100
#     cr.plot(kind='bar', stacked=True)
#     plt.title(f"{col} vs Churn (%)")
#     plt.show()

for col in cat_cols:
    if col != 'Churn':
        table = pd.crosstab(df_dup[col], df_dup['Churn'])
        _, p, _, _ = chi2_contingency(table)
        print(f"{col} → p-value: {p:.5f}")


# =========================================
# 🧹 CLEANING
# =========================================
df.drop(columns=['customerID'], inplace=True)

df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df['TotalCharges']=df['TotalCharges'].fillna(df['TotalCharges'].median())


# =========================================
# ⚙️ FEATURE ENGINEERING (IMPROVED)
# =========================================

# Core financial behavior
df['Charges_per_tenure'] = df['MonthlyCharges'] / (df['tenure'] + 1)
df['TotalCharges_log'] = np.log1p(df['TotalCharges'])

# Risk features
df['High_Spender'] = (df['MonthlyCharges'] > df['MonthlyCharges'].median()).astype(int)

df['high_risk'] = (
    (df['MonthlyCharges'] > df['MonthlyCharges'].quantile(0.7)) &
    (df['tenure'] < df['tenure'].quantile(0.3))
).astype(int)

# Tenure grouping (VERY IMPORTANT)
df['tenure_group'] = pd.cut(
    df['tenure'],
    bins=[0,12,24,48,72],
    labels=[0,1,2,3],include_lowest=True
)
df['tenure_group']=df['tenure_group'].astype(int)

# Contract risk
df['Contract_Risk'] = df['Contract'].map({
    'Month-to-month': 2,
    'One year': 1,
    'Two year': 0
})

# Service count (FIXED)
service_cols = [
    'PhoneService','MultipleLines','OnlineSecurity','OnlineBackup',
    'DeviceProtection','TechSupport','StreamingTV','StreamingMovies'
]

df['Total_Services'] = df[service_cols].apply(
    lambda x: x.isin(['Yes']).sum(), axis=1
)


# =========================================
# 🎯 TARGET
# =========================================
df['Churn'] = df['Churn'].map({'Yes':1, 'No':0})


# =========================================
# 🔄 ENCODING
# =========================================
cat_cols = df.select_dtypes(include='object').columns
df = pd.get_dummies(df, columns=cat_cols, drop_first=True)


# =========================================
# 📉 CORRELATION
# =========================================
plt.figure(figsize=(12,8))
sns.heatmap(df.corr(), cmap='coolwarm')
plt.title("Correlation Matrix")
plt.show()


df.to_csv("cleaned_data.csv",index=False)
