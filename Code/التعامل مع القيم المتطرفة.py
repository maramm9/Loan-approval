Q1 = df['ApplicantIncome'].quantile(0.25)
Q3 = df['ApplicantIncome'].quantile(0.75)
IQR = Q3 - Q1
df = df[~((df['ApplicantIncome'] < (Q1 - 1.5 * IQR)) | (df['ApplicantIncome'] > (Q3 + 1.5 * IQR)))]