import joblib
import pandas as pd
df=pd.read_csv(r"data\cleaned_data.csv")
X=df.drop(columns=['Churn'])
joblib.dump(X.columns, "columns.pkl")