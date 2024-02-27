from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import time

app = Flask(__name__)

# Configure MySQL connection details
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root_password'
app.config['MYSQL_DB'] = 'mydatabase'
app.config['MYSQL_PORT'] = 3307


mysql = MySQL(app)

# Define a function to create the table in the database
def create_table():
    cur = mysql.connection.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL
                  )''')
    mysql.connection.commit()
    cur.close()

# Define a function to connect to the database with retries
def connect_to_database(retries=5, delay=1):
    for _ in range(retries):
        try:
            mysql.connection.ping()
            return True
        except Exception as e:
            print(f"Failed to connect to database: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
    return False

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        cur.close()
        if user:
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    with app.app_context():
        create_table()
        if not connect_to_database():
            print("Failed to connect to the database. Exiting...")
            exit(1)
    app.run(debug=True, host='0.0.0.0')
