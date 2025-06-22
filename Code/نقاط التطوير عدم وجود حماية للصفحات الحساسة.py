# إضافة ديكوراتور للتحقق من الصلاحيات
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            flash('يجب تسجيل الدخول أولاً', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# تطبيق على الصفحات الحساسة:
@app.route("/manage-request")
@login_required
def manage_request(): 
    ...