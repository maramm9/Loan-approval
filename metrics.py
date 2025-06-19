import pandas as pd
import pickle
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def get_model_metrics(csv_path="loan_prediction.csv"):
    # Load and preprocess data (using the more thorough approach from the second script)
    df = pd.read_csv(csv_path)
    
    # Data cleaning and encoding
    df["Loan_Status"] = df["Loan_Status"].map({"Y": 1, "N": 0})
    df["Gender"] = df["Gender"].map({"Male": 1, "Female": 0}).fillna(1)
    df["Married"] = df["Married"].map({"Yes": 1, "No": 0}).fillna(1)
    df["Education"] = df["Education"].map({"Graduate": 0, "Not Graduate": 1})
    df["Self_Employed"] = df["Self_Employed"].map({"Yes": 1, "No": 0}).fillna(0)
    df["Dependents"] = df["Dependents"].replace("3+", 3).astype(float).fillna(0)
    df["LoanAmount"] = df["LoanAmount"].fillna(df["LoanAmount"].median())
    df["Loan_Amount_Term"] = df["Loan_Amount_Term"].fillna(360.0)
    df["Credit_History"] = df["Credit_History"].fillna(1.0)
    
    # One-hot encode Property_Area
    df["Property_Area_Urban"] = (df["Property_Area"] == "Urban").astype(int)
    df["Property_Area_Rural"] = (df["Property_Area"] == "Rural").astype(int)
    df["Property_Area_Semiurban"] = (df["Property_Area"] == "Semiurban").astype(int)

    # Select features - you can choose either the limited set or full set:
    # Limited features (original approach):
    # X = df[['Gender', 'Married', 'Education', 'ApplicantIncome', 'LoanAmount']]
    
    # Full features (recommended):
    X = df[["Gender", "Married", "Dependents", "Education", "Self_Employed",
            "ApplicantIncome", "CoapplicantIncome", "LoanAmount",
            "Loan_Amount_Term", "Credit_History",
            "Property_Area_Urban", "Property_Area_Rural", "Property_Area_Semiurban"]]
    
    y = df["Loan_Status"]

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Save the model (optional)
    with open("model.pkl", "wb") as f:
        pickle.dump(model, f)

    # Generate predictions and metrics
    y_pred = model.predict(X_test)
    report_dict = classification_report(y_test, y_pred, output_dict=True)

    return {
        "accuracy": round(report_dict["accuracy"], 3),
        "precision": round(report_dict["1"]["precision"], 3),
        "recall": round(report_dict["1"]["recall"], 3),
        "f1": round(report_dict["1"]["f1-score"], 3),
    }