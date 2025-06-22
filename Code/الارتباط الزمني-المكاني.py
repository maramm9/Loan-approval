# المزيج السحري بين التاريخ والمنطقة
cross_tab = pd.crosstab(
    index=data['Property_Area'],
    columns=data['Loan_Application_Date'].dt.quarter,
    values=data['Loan_Status'],
    aggfunc='mean'
)

sns.heatmap(cross_tab, annot=True, fmt=".0%")