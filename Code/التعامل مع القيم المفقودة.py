from sklearn.impute import SimpleImputer
# للأرقام
num_imputer = SimpleImputer(strategy='median')
df[['LoanAmount']] = num_imputer.fit_transform(df[['LoanAmount']])
# للفئات
cat_imputer = SimpleImputer(strategy='most_frequent')
df[['Credit_History']] = cat_imputer.fit_transform(df[['Credit_History']])