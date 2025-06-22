# اختبارات الجودة الصارمة
assert data['Loan_Application_Date'].isnull().sum() == 0, "يوجد تواريخ مفقودة!"
assert (data['Loan_Application_Date'] > today).sum() == 0, "يوجد تواريخ مستقبلية!"
assert data['Loan_Application_Date'].min().year >= 2000, "يوجد تواريخ قديمة غير واقعية!"

# اختبار الترميز الدوري
assert np.allclose(data['Month_sin']**2 + data['Month_cos']**2, 1), "الترميز الدوري غير دقيق!"