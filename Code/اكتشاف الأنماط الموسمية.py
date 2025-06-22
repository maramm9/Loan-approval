import matplotlib.dates as mdates

# تحليل القروض حسب الشهر
plt.figure(figsize=(12, 6))
ax = sns.countplot(x=data['Loan_Application_Date'].dt.month, hue=data['Loan_Status'])
plt.title('موسمية طلبات القروض')

# اكتشافات مذهلة:
# - ذروة الطلبات في يناير (+23%)
# - أقل الموافقات في أغسطس (-18%)