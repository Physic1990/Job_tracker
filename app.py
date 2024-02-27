from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import time

app = Flask(__name__)

# Configure MySQL connection details
db_config = {
    'host': 'db',
    'user': 'root',
    'password': 'root_password',
    'database': 'mydatabase',
    'port': 3307,
}

# Function to create the users table if not exists
def create_table():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(255) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL
                      )''')
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print("Failed to create table: {}".format(err))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            if user:
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', error='Invalid username or password')
        except mysql.connector.Error as err:
            print("Failed to fetch user: {}".format(err))
            return render_template('login.html', error='Failed to fetch user')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            print("Failed to insert user: {}".format(err))
            return render_template('signup.html', error='Failed to insert user')
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    with app.app_context():
        create_table()
    app.run(debug=True, host='0.0.0.0')
