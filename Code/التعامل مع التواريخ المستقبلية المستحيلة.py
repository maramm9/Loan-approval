# اكتشاف تواريخ بعد سنة 2025 (مستقبلية)!
today = pd.Timestamp.now()
future_dates_mask = data['Loan_Application_Date'] > today

# استبدالها بمنوال الشهر
month_mode = data['Loan_Application_Date'].dt.month.mode()[0]
data.loc[future_dates_mask, 'Loan_Application_Date'] = data.loc[future_dates_mask, 'Loan_Application_Date'].apply(
    lambda x: x.replace(month=month_mode, year=today.year - 1))