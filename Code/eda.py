import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import os
from sklearn.preprocessing import LabelEncoder

# ======================
# 1. Data Loading
# ======================
df = pd.read_csv("C:/Users/باسل/OneDrive/Desktop/my_part/loan_prediction.csv", encoding="utf-8")

print("تم تحميل البيانات بنجاح!")
print(f"عدد الصفوف: {len(df)}، عدد الأعمدة: {len(df.columns)}")
df.head()

# ======================
# 2. Data Cleaning
# ======================
# التحقق من الصفوف المكررة
duplicates = df.duplicated().sum()
print(f"عدد الصفوف المكررة: {duplicates}")

# معلومات عن البيانات
print("\nمعلومات عن مجموعة البيانات:")
df.info()

# القيم المفقودة
print("\nالقيم المفقودة:")
print(df.isnull().sum())

# التعامل مع القيم المفقودة
# البيانات العددية
df['LoanAmount'] = df['LoanAmount'].fillna(df['LoanAmount'].median()) 
df['Loan_Amount_Term'] = df['Loan_Amount_Term'].fillna(df['Loan_Amount_Term'].mean())
df['Credit_History'] = df['Credit_History'].fillna(df['Credit_History'].mode()[0])

# البيانات الفئوية
df['Gender'] = df['Gender'].fillna(df['Gender'].mode()[0]) 
df['Married'] = df['Married'].fillna(df['Married'].mode()[0])
df['Dependents'] = df['Dependents'].fillna(df['Dependents'].mode()[0])
df['Self_Employed'] = df['Self_Employed'].fillna(df['Self_Employed'].mode()[0]) 

# التحقق من عدم وجود قيم مفقودة بعد المعالجة
print("\nالقيم المفقودة بعد المعالجة:")
print(df.isnull().sum())

# ======================
# 3. معالجة التاريخ المتقدمة
# ======================
def smart_date_parser(date_str):
    """دالة ذكية لتحويل تنسيقات التاريخ المختلفة"""
    formats = ['%d/%m/%Y', '%m/%d/%Y', '%Y-%m-%d', '%b %d, %Y']
    for fmt in formats:
        try:
            return pd.to_datetime(date_str, format=fmt)
        except:
            continue
    return pd.NaT

# تطبيق معالجة التاريخ إذا كان العمود موجوداً
if 'Application_Date' in df.columns:
    # تحويل التاريخ
    df['Application_Date'] = df['Application_Date'].apply(smart_date_parser)
    
    # معالجة التواريخ المستقبلية
    today = datetime.now()
    future_mask = df['Application_Date'] > today
    df.loc[future_mask, 'Application_Date'] = df.loc[future_mask, 'Application_Date'].apply(
        lambda x: x.replace(year=today.year-1))
    
    # توليد ميزات زمنية جديدة
    df['Day_of_Year'] = df['Application_Date'].dt.dayofyear
    df['Quarter'] = df['Application_Date'].dt.quarter
    df['Application_Age_Days'] = (today - df['Application_Date']).dt.days
    df['Month_sin'] = np.sin(2 * np.pi * df['Application_Date'].dt.month/12)
    df['Month_cos'] = np.cos(2 * np.pi * df['Application_Date'].dt.month/12)
    
    print("\nتم معالجة البيانات الزمنية بنجاح!")
    print("الميزات الجديدة المضافة:")
    print(df[['Application_Date', 'Day_of_Year', 'Quarter', 'Application_Age_Days', 'Month_sin', 'Month_cos']].head())
else:
    print("\nتحذير: لا يوجد عمود 'Application_Date' للتحليل الزمني")

# ======================
# 4. التحليل الاستكشافي الأساسي
# ======================
# إنشاء مجلد لحفظ الصور
os.makedirs('static/images', exist_ok=True)

# توزيع المتغيرات الفئوية
cat_cols = ['Gender', 'Married', 'Education', 'Self_Employed', 'Property_Area', 'Dependents', 'Loan_Status','Credit_History']
for col in cat_cols:
    print(f"\nتوزيع {col}:")
    print(df[col].value_counts())
    
    plt.figure(figsize=(8, 5))
    sns.countplot(x=col, data=df)
    plt.title(f'توزيع {col}')
    plt.xticks(rotation=45)
    plt.savefig(f'static/images/{col}_Distribution.png', bbox_inches='tight')
    plt.close()  # إغلاق الشكل لتجنب عرضه في البيئة التفاعلية

# توزيع متغير الهدف (Loan_Status)
print("\nتوزيع متغير الهدف (Loan_Status):")
print(df['Loan_Status'].value_counts())
plt.figure(figsize=(8, 5))
sns.countplot(x='Loan_Status', data=df)
plt.title("توزيع الموافقة على القروض")
plt.savefig('static/images/Loan_Status_Distribution.png', bbox_inches='tight')
plt.close()

# توزيع المتغيرات العددية
num_cols = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount']
for col in num_cols:
    plt.figure(figsize=(10, 6))
    sns.histplot(df[col], kde=True)
    plt.title(f'توزيع {col}')
    plt.savefig(f'static/images/{col}_Distribution.png', bbox_inches='tight')
    plt.close()

# خريطة الارتباط
df_numeric = df.select_dtypes(include=['int64', 'float64'])
plt.figure(figsize=(12, 8))
sns.heatmap(df_numeric.corr(), annot=True, cmap='coolwarm', fmt='.2f')
plt.title('خريطة الارتباط للمتغيرات العددية')
plt.savefig('static/images/Correlation_Heatmap.png', bbox_inches='tight')
plt.close()

# ======================
# 5. Feature Engineering
# ======================
# إنشاء الدخل الكلي
df['Total_Income'] = df['ApplicantIncome'] + df['CoapplicantIncome']

# التوزيع قبل التحويل
plt.figure(figsize=(10, 6))
sns.histplot(df['Total_Income'], kde=True)
plt.title('توزيع الدخل الكلي (قبل التحويل)')
plt.savefig('static/images/Total_Income_Before_Log.png', bbox_inches='tight')
plt.close()

# تطبيق التحويل اللوغاريتمي
df['Log_Total_Income'] = np.log1p(df['Total_Income'])

# التوزيع بعد التحويل
plt.figure(figsize=(10, 6))
sns.histplot(df['Log_Total_Income'], kde=True)
plt.title('توزيع الدخل الكلي (بعد التحويل)')
plt.savefig('static/images/Total_Income_After_Log.png', bbox_inches='tight')
plt.close()

# التحويل اللوغاريتمي لمبلغ القرض
plt.figure(figsize=(10, 6))
sns.histplot(df['LoanAmount'], kde=True)
plt.title('توزيع مبلغ القرض (قبل التحويل)')
plt.savefig('static/images/LoanAmount_Before_Log.png', bbox_inches='tight')
plt.close()

df['Log_LoanAmount'] = np.log1p(df['LoanAmount'])

plt.figure(figsize=(10, 6))
sns.histplot(df['Log_LoanAmount'], kde=True)
plt.title('توزيع مبلغ القرض (بعد التحويل)')
plt.savefig('static/images/LoanAmount_After_Log.png', bbox_inches='tight')
plt.close()

# التحويل اللوغاريتمي لمدة القرض
df['Log_Loan_Amount_Term'] = np.log1p(df['Loan_Amount_Term'])

# حذف الأعمدة غير الضرورية
cols_to_drop = ['ApplicantIncome','CoapplicantIncome','Total_Income','Loan_Amount_Term','LoanAmount','Loan_ID']
existing_cols = [col for col in cols_to_drop if col in df.columns]
df = df.drop(columns=existing_cols)

print("\nتمت هندسة الميزات بنجاح!")
df.head()

# ======================
# 6. التحليل الزمني المتقدم
# ======================
def comprehensive_date_analysis():
    """دالة للتحليل الزمني المتقدم"""
    # 1. التوزيع الشهري للطلبات
    plt.figure(figsize=(14, 7))
    monthly_counts = df['Application_Date'].dt.month.value_counts().sort_index()
    months = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو',
             'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
    monthly_counts.index = [months[i-1] for i in monthly_counts.index]
    
    sns.barplot(x=monthly_counts.index, y=monthly_counts.values, palette="viridis")
    plt.title('التوزيع الشهري لطلبات القروض')
    plt.xlabel('الشهر')
    plt.ylabel('عدد الطلبات')
    plt.xticks(rotation=45)
    plt.savefig('static/images/monthly_distribution.png', bbox_inches='tight')
    plt.close()

    # 2. الموسمية في الموافقات
    monthly_data = df.groupby(df['Application_Date'].dt.month).agg({
        'Loan_Status': 'mean',
    }).reset_index()
    
    plt.figure(figsize=(14, 7))
    sns.lineplot(x=monthly_data['Application_Date'], y=monthly_data['Loan_Status']*100, 
                 marker='o', linewidth=2.5, color='#2ecc71')
    plt.fill_between(monthly_data['Application_Date'], monthly_data['Loan_Status']*100,
                     alpha=0.1, color='#2ecc71')
    plt.title('الموسمية في معدلات الموافقة على القروض')
    plt.xlabel('الشهر')
    plt.ylabel('نسبة الموافقة (%)')
    plt.grid(alpha=0.2)
    plt.savefig('static/images/approval_seasonality.png', bbox_inches='tight')
    plt.close()

    # 3. خريطة حرارة ربعية
    pivot = df.pivot_table(
        index='Property_Area',
        columns='Quarter',
        values='Loan_Status',
        aggfunc='mean',
        fill_value=0
    )
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot, annot=True, fmt=".0%", cmap="YlGnBu", 
                linewidths=.5, cbar_kws={'label': 'نسبة الموافقة'})
    plt.title('معدلات الموافقة حسب المنطقة والربع')
    plt.savefig('static/images/quarterly_heatmap.png', bbox_inches='tight')
    plt.close()

    # 4. الارتباط الزمني-المكاني
    df['Quarter'] = df['Application_Date'].dt.quarter
    cross_tab = pd.crosstab(
        index=df['Property_Area'],
        columns=df['Quarter'],
        values=df['Loan_Status'],
        aggfunc='mean',
        dropna=False
    )
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(cross_tab, annot=True, fmt=".0%", cmap="coolwarm")
    plt.title('الارتباط الزمني-المكاني للموافقات')
    plt.savefig('static/images/spatio_temporal.png', bbox_inches='tight')
    plt.close()

# تنفيذ التحليل الزمني إذا كان عمود التاريخ موجوداً
if 'Application_Date' in df.columns:
    print("\nبدء التحليل الزمني المتقدم...")
    comprehensive_date_analysis()
    print("تم الانتهاء من التحليل الزمني وحفظ الرسوم البيانية في static/images/")
else:
    print("\nتخطي التحليل الزمني لعدم وجود عمود التاريخ")

# ======================
# 7. ترميز المتغيرات الفئوية
# ======================
# تحويل البيانات الفئوية إلى رقمية
cat_cols = ['Gender','Married','Education','Self_Employed','Dependents','Property_Area','Loan_Status']
le = LabelEncoder()

for col in cat_cols:
    if col in df.columns:
        df[col] = le.fit_transform(df[col])

print("\nتم ترميز المتغيرات الفئوية بنجاح!")
df.head()
print("\nأنواع البيانات بعد الترميز:")
print(df.dtypes)

# ======================
# 8. إعداد البيانات للنمذجة
# ======================
# تقسيم البيانات إلى متغيرات مستقلة وتابعة
X = df.drop('Loan_Status', axis=1)  # المتغيرات المستقلة
Y = df['Loan_Status']               # المتغير التابع

print("\nشكل البيانات النهائية:")
print(f"المتغيرات المستقلة (X): {X.shape}")
print(f"المتغير التابع (Y): {Y.shape}")

# ======================
# 9. حفظ البيانات المعالجة
# ======================
df.to_csv('cleaned_loan_data.csv', index=False)
print("\nتم حفظ البيانات المعالجة في cleaned_loan_data.csv")

print("\nتم تنفيذ جميع الخطوات بنجاح!")