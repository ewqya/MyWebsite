from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# 初始化数据库
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# 首页路由
@app.route('/')
def home():
    welcome_message = "Welcome to My Flask Website!"
    services = ["Web Development", "SEO Optimization", "Digital Marketing"]
    return render_template('index.html', message=welcome_message, services=services)

# 关于页面路由
@app.route('/about')
def about():
    return render_template('about.html')

# 注册页面路由
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        try:
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, password))
            conn.commit()
            conn.close()
            return "Registration successful!"
        except sqlite3.IntegrityError:
            return "Email already registered. Please try another."
    return render_template('register.html')

# 登录页面路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
        user = c.fetchone()
        conn.close()
        if user:
            return f"Welcome back, {user[1]}!"
        else:
            return "Invalid credentials. Please try again."
    return render_template('login.html')

# 用户列表页面路由
@app.route('/users')
def users():
    page = int(request.args.get('page', 1))
    limit = 5
    offset = (page - 1) * limit
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users LIMIT ? OFFSET ?', (limit, offset))
    users = c.fetchall()
    conn.close()
    return render_template('users.html', users=users, page=page)

# 服务页面路由
@app.route('/services')
def services():
    return render_template('services.html')

# 主函数，适配 Railway
if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))  # Railway 动态分配端口
    app.run(host="0.0.0.0", port=port)
