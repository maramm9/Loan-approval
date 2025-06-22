# إضافة هذا الراوت لحذف الطلبات
@app.route('/delete_request/<int:index>', methods=['POST'])
def delete_request(index):
    if 0 <= index < len(submitted_requests):
        del submitted_requests[index]
        flash('تم حذف الطلب بنجاح', 'success')
    else:
        flash('فشل في حذف الطلب: رقم غير صحيح', 'error')
    return redirect(url_for('manage_request'))