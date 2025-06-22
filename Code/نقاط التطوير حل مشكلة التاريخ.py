# إضافة صفحة مخصصة
@app.route("/date_issue")
def date_issue():
    explanation = """
    المشكلة: تواريخ غير متسقة في مجموعة البيانات (تنسيقات مختلفة: dd/mm/yyyy, mm/dd/yyyy)
    الحل:
    1. تحويل جميع التواريخ إلى تنسيق موحد (ISO 8601)
    2. معالجة التواريخ الفارغة باستخدام interpolation زمني
    3. إنشاء متغيرات جديدة (يوم/شهر/سنة) للتحليل
    """
    return render_template("date_issue.html", explanation=explanation)