from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Yashk25@root",
    database="user_registration"
)

cursor = db.cursor()

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['userId']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE userId=%s AND password=%s", (user_id, password))
        user = cursor.fetchone()
        if user:
            session['user'] = user_id
            return redirect('/welcome')
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['userId']
        mobile_number = request.form['mobileNumber']
        password = request.form['password']
        cursor.execute("INSERT INTO users (userId, mobileNumber, password) VALUES (%s, %s, %s)",
                       (user_id, mobile_number, password))
        db.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/welcome')
def welcome():
    if 'user' in session:
        cursor.execute("SELECT course_code, course_name, credits FROM courses")
        courses = cursor.fetchall()
        course_list = [{'course_code': row[0], 'course_name': row[1], 'credits': row[2]} for row in courses]
        return render_template('welcome.html', courses=course_list)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
