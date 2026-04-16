import joblib
import pandas as pd
df=pd.read_csv(r"data\WA_Fn-UseC_-Telco-Customer-Churn.csv")
X=df.drop(columns=['Churn'])
joblib.dump(X.columns, "columns.pkl")