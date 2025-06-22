# الخطأ: استخدام ميزات غير متوافقة مع تطبيق Flask
# في app.py: [gender, married, ...] + area (3 قيم)
# في metrics.py: 13 ميزة (بما فيها Property_Area)

# الحل: توحيد الميزات
X = df[[
    "Gender", "Married", "Dependents", "Education", "Self_Employed",
    "ApplicantIncome", "CoapplicantIncome", "LoanAmount",
    "Loan_Amount_Term", "Credit_History"
]]