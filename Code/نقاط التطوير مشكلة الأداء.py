# الحل: فصل عملية التدريب عن التقييم
def train_and_save_model(csv_path="loan_prediction.csv"):
    # ... (نفس كود معالجة البيانات)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    
    # حفظ النموذج وبيانات الاختبار
    pickle.dump(model, open("model.pkl", "wb"))
    X_test.to_pickle("X_test.pkl")
    y_test.to_pickle("y_test.pkl")

def get_model_metrics():
    # تحميل النموذج وبيانات الاختبار
    model = pickle.load(open("model.pkl", "rb"))
    X_test = pd.read_pickle("X_test.pkl")
    y_test = pd.read_pickle("y_test.pkl")
    
    # ... (باقي الكود)