import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# 1. تحميل البيانات
data = pd.read_csv("loan_data.csv")

# 2. فك شيفرة التواريخ المختلطة
def parse_dates(date_str):
    formats = ['%d/%m/%Y', '%m/%d/%Y', '%Y-%m-%d', '%b %d, %Y']
    for fmt in formats:
        try:
            return pd.to_datetime(date_str, format=fmt)
        except:
            continue
    return pd.NaT

data['Application_Date'] = data['Raw_Date'].apply(parse_dates)

# 3. معالجة التواريخ المستقبلية
current_year = datetime.now().year
future_mask = data['Application_Date'].dt.year > current_year
data.loc[future_mask, 'Application_Date'] = data.loc[future_mask, 'Application_Date'].apply(
    lambda x: x.replace(year=current_year-1))

# 4. توليد الميزات الزمنية
data['Day_of_Year'] = data['Application_Date'].dt.dayofyear
data['Quarter'] = data['Application_Date'].dt.quarter
data['Application_Age_Days'] = (datetime.now() - data['Application_Date']).dt.days

# 5. الترميز الدوري للشهور
data['Month_sin'] = np.sin(2 * np.pi * data['Application_Date'].dt.month/12)
data['Month_cos'] = np.cos(2 * np.pi * data['Application_Date'].dt.month/12)

# 6. التحليل الموسمي
def plot_seasonality():
    monthly_data = data.groupby(data['Application_Date'].dt.month).agg({
        'Loan_Status': 'mean',
        'Loan_ID': 'count'
    }).rename(columns={'Loan_ID': 'Applications'})
    
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # تطبيقات القروض
    ax1.bar(monthly_data.index, monthly_data['Applications'], 
            color='skyblue', alpha=0.7, label='الطلبات')
    ax1.set_xlabel('الشهر')
    ax1.set_ylabel('عدد الطلبات', color='skyblue')
    ax1.tick_params(axis='y', labelcolor='skyblue')
    
    # معدل الموافقة
    ax2 = ax1.twinx()
    ax2.plot(monthly_data.index, monthly_data['Loan_Status']*100, 
             'r-o', linewidth=2, label='معدل الموافقة')
    ax2.set_ylabel('نسبة الموافقة (%)', color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    
    plt.title('الموسمية في طلبات القروض')
    fig.legend(loc='upper right')
    plt.savefig('seasonality.png', bbox_inches='tight')

# 7. خريطة الحرارة الربعية
def plot_quarterly_heatmap():
    pivot = data.pivot_table(
        index='Property_Area',
        columns='Quarter',
        values='Loan_Status',
        aggfunc='mean'
    )
    
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot, annot=True, fmt=".0%", cmap="YlGnBu",
                cbar_kws={'label': 'نسبة الموافقة'})
    plt.title('معدلات الموافقة حسب المنطقة والربع')
    plt.savefig('quarterly_heatmap.png', bbox_inches='tight')

# 8. تحليل الارتباط الزمني-المكاني
def spatio_temporal_analysis():
    cross_tab = pd.crosstab(
        index=data['Property_Area'],
        columns=data['Application_Date'].dt.quarter,
        values=data['Loan_Status'],
        aggfunc='mean'
    )
    
    plt.figure(figsize=(10, 6))
    sns.heatmap(cross_tab, annot=True, fmt=".0%", cmap="coolwarm")
    plt.title('الارتباط الزمني-المكاني للموافقات')
    plt.savefig('spatio_temporal.png', bbox_inches='tight')

# 9. التوزيع الزمني للقيم المتطرفة
def plot_outliers_timeline():
    plt.figure(figsize=(12, 6))
    
    # تطبيقات عادية
    normal = data[data['ApplicantIncome'] <= data['ApplicantIncome'].quantile(0.95)]
    plt.scatter(normal['Application_Date'], normal['ApplicantIncome'],
                alpha=0.5, label='تطبيقات عادية')
    
    # قيم متطرفة
    outliers = data[data['ApplicantIncome'] > data['ApplicantIncome'].quantile(0.95)]
    plt.scatter(outliers['Application_Date'], outliers['ApplicantIncome'],
                color='red', s=80, label='قيم متطرفة')
    
    plt.title('التوزيع الزمني للقيم المتطرفة في الدخل')
    plt.ylabel('دخل مقدم الطلب')
    plt.legend()
    plt.savefig('outliers_timeline.png', bbox_inches='tight')

# 10. التحليل الشامل
def comprehensive_date_analysis():
    plot_seasonality()
    plot_quarterly_heatmap()
    spatio_temporal_analysis()
    plot_outliers_timeline()
    
    # تحليل إضافي
    fig, ax = plt.subplots(2, 2, figsize=(15, 10))
    
    # التوزيع الشهري
    data['Application_Date'].dt.month.value_counts().sort_index().plot(
        kind='bar', ax=ax[0, 0], color='teal')
    ax[0, 0].set_title('التوزيع الشهري للطلبات')
    
    # العمر الزمني للطلبات
    data['Application_Age_Days'].hist(bins=30, ax=ax[0, 1], color='purple')
    ax[0, 1].set_title('توزيع عمر الطلبات (أيام)')
    
    # العلاقة بين الموسم ومبلغ القرض
    sns.boxplot(x='Quarter', y='LoanAmount', data=data, ax=ax[1, 0])
    ax[1, 0].set_title('مبالغ القروض حسب الربع')
    
    # الترميز الدوري
    sns.scatterplot(x='Month_sin', y='Month_cos', 
                    hue='Loan_Status', data=data, ax=ax[1, 1])
    ax[1, 1].set_title('التمثيل الدوري للشهور')
    
    plt.tight_layout()
    plt.savefig('comprehensive_date_analysis.png', bbox_inches='tight')

# تنفيذ التحليل
if __name__ == "__main__":
    comprehensive_date_analysis()