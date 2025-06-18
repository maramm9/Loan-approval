# retrain_model.py
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

df = pd.read_csv("loan_prediction.csv")
df["Loan_Status"] = df["Loan_Status"].map({"Y": 1, "N": 0})
df["Gender"] = df["Gender"].map({"Male": 1, "Female": 0}).fillna(1)
df["Married"] = df["Married"].map({"Yes": 1, "No": 0}).fillna(1)
df["Education"] = df["Education"].map({"Graduate": 0, "Not Graduate": 1})
df["Self_Employed"] = df["Self_Employed"].map({"Yes": 1, "No": 0}).fillna(0)
df["Dependents"] = df["Dependents"].replace("3+", 3).astype(float).fillna(0)
df["LoanAmount"] = df["LoanAmount"].fillna(df["LoanAmount"].median())
df["Loan_Amount_Term"] = df["Loan_Amount_Term"].fillna(360.0)
df["Credit_History"] = df["Credit_History"].fillna(1.0)

df["Property_Area_Urban"] = (df["Property_Area"] == "Urban").astype(int)
df["Property_Area_Rural"] = (df["Property_Area"] == "Rural").astype(int)
df["Property_Area_Semiurban"] = (df["Property_Area"] == "Semiurban").astype(int)

X = df[["Gender", "Married", "Dependents", "Education", "Self_Employed",
        "ApplicantIncome", "CoapplicantIncome", "LoanAmount",
        "Loan_Amount_Term", "Credit_History",
        "Property_Area_Urban", "Property_Area_Rural", "Property_Area_Semiurban"]]
y = df["Loan_Status"]

model = RandomForestClassifier()
model.fit(X, y)

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)


