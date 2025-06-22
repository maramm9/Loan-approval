# تحويل الأشهر إلى إحداثيات دائرية
data['Month_sin'] = np.sin(2 * np.pi * data['Loan_Application_Date'].dt.month/12)
data['Month_cos'] = np.cos(2 * np.pi * data['Loan_Application_Date'].dt.month/12)