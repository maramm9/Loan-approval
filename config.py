# استبدال SQLite بـ PostgreSQL
import os
import psycopg2

# إعداد متغير البيئة في Netlify
DATABASE_URL = os.environ.get('DATABASE_URL')

# الاتصال
conn = psycopg2.connect(DATABASE_URL, sslmode='require')