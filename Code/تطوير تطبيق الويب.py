import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# تحميل النموذج والبيانات
model = RandomForestClassifier()
# ... (تدريب النموذج هنا)

st.title("نظام الموافقة على القروض")
st.write("أدخل بيانات العميل:")

# حقول إدخال البيانات
income = st.number_input("الدخل الشهري")
loan_amount = st.number_input("مبلغ القرض")
credit_history = st.selectbox("السجل الائتماني", [1, 0])

if st.button("تنبؤ"):
    input_data = pd.DataFrame([[income, loan_amount, credit_history]], 
                             columns=['ApplicantIncome', 'LoanAmount', 'Credit_History'])
    prediction = model.predict(input_data)[0]
    st.success("موافق" if prediction == 1 else "مرفوض")