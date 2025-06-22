data['Day_of_Year'] = data['Loan_Application_Date'].dt.dayofyear
data['Is_Quarter_End'] = data['Loan_Application_Date'].dt.is_quarter_end.astype(int)