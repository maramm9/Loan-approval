# إضافة معالجة للدخل (تطبيع)
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
income_features = ["ApplicantIncome", "CoapplicantIncome", "LoanAmount"]
X_train[income_features] = scaler.fit_transform(X_train[income_features])
X_test[income_features] = scaler.transform(X_test[income_features])