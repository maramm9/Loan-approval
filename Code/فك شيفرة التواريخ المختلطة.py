# اكتشاف 4 تنسيقات مختلفة للتاريخ!
date_formats = [
    '%d/%m/%Y',   # 25/12/2023
    '%m/%d/%Y',   # 12/25/2023
    '%Y-%m-%d',   # 2023-12-25
    '%b %d, %Y'  # Dec 25, 2023
]

def smart_date_parser(date_str):
    for fmt in date_formats:
        try:
            return pd.to_datetime(date_str, format=fmt)
        except ValueError:
            pass
    return pd.NaT  # للتواريخ غير القابلة للتحويل

data['Loan_Application_Date'] = data['Date_Column'].apply(smart_date_parser)