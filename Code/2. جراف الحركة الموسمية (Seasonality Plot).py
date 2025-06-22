import matplotlib.pyplot as plt
import seaborn as sns

# بيانات موسمية افتراضية
months = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو',
          'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
applications = [120, 115, 130, 125, 140, 135, 110, 95, 105, 145, 160, 155]
approvals = [84, 80, 91, 88, 98, 95, 66, 57, 74, 102, 112, 109]

plt.figure(figsize=(14, 7))
sns.lineplot(x=months, y=applications, marker='o', label='الطلبات', linewidth=2.5, color='#3498db')
sns.lineplot(x=months, y=approvals, marker='s', label='الموافقات', linewidth=2.5, color='#2ecc71')

# إضافة تأثيرات بصرية
plt.fill_between(months, applications, alpha=0.1, color='#3498db')
plt.fill_between(months, approvals, alpha=0.1, color='#2ecc71')

# إبراز الذروة والموسم المنخفض
plt.annotate('ذروة الطلبات +23%', xy=('نوفمبر', 160), 
             xytext=('سبتمبر', 170), arrowprops=dict(arrowstyle='->'))
plt.annotate('أقل موافقات -18%', xy=('أغسطس', 57), 
             xytext=('يونيو', 40), arrowprops=dict(arrowstyle='->'))

plt.title('الموسمية في طلبات القروض', fontsize=16)
plt.xlabel('الشهر')
plt.ylabel('عدد الطلبات')
plt.legend()
plt.grid(alpha=0.2)
plt.tight_layout()