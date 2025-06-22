# في metrics.py
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

def get_model_metrics():
    # يجب استبدال هذا ببيانات حقيقية من الاختبار
    y_true = [0, 1, 0, 1, 1]
    y_pred = [0, 1, 0, 0, 1]
    
    return {
        "precision": precision_score(y_true, y_pred),
        "recall": recall_score(y_true, y_pred),
        "f1": f1_score(y_true, y_pred),
        "accuracy": accuracy_score(y_true, y_pred)
    }