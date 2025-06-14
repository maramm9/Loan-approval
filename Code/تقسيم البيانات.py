from sklearn.model_selection import train_test_split
X = df.drop(['Loan_Status', 'Loan_ID'], axis=1)  # الميزات
y = df['Loan_Status']  # الهدف
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)