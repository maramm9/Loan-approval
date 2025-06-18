import pandas as pd
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def get_model_metrics(csv_path="loan_prediction.csv"):
    df = pd.read_csv(csv_path)
    df = df.dropna()

    df['Gender'] = df['Gender'].map({'Male': 1, 'Female': 0})
    df['Married'] = df['Married'].map({'Yes': 1, 'No': 0})
    df['Education'] = df['Education'].map({'Graduate': 1, 'Not Graduate': 0})
    df['Self_Employed'] = df['Self_Employed'].map({'Yes': 1, 'No': 0})
    df['Loan_Status'] = df['Loan_Status'].map({'Y': 1, 'N': 0})

    X = df[['Gender', 'Married', 'Education', 'ApplicantIncome', 'LoanAmount']]
    y = df['Loan_Status']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    report_dict = classification_report(y_test, y_pred, output_dict=True)

    return {
        "accuracy": round(report_dict["accuracy"], 3),
        "precision": round(report_dict["1"]["precision"], 3),
        "recall": round(report_dict["1"]["recall"], 3),
        "f1": round(report_dict["1"]["f1-score"], 3),
    }
