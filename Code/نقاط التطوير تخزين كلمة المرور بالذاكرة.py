# الحل: استخدام قاعدة بيانات بسيطة (SQLite)
import sqlite3
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (email TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()