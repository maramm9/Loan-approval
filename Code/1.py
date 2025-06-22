# الخطوة 2: التنظيف الاستراتيجي
from sklearn.impute import SimpleImputer

# حل لغز القيم الفارغة
income_imputer = SimpleImputer(strategy='median')
data['CoapplicantIncome'] = income_imputer.fit_transform(data[['CoapplicantIncome']])

# مواجهة الوحش المتطرف!
data['Log_ApplicantIncome'] = np.log1p(data['ApplicantIncome'])

# إصلاح الاختلال بالعينة المتوازنة
from imblearn.under_sampling import RandomUnderSampler
rus = RandomUnderSampler(random_state=42)
X_res, y_res = rus.fit_resample(data[features], data['Loan_Status'])