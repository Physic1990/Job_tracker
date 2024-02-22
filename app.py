from flask import Flask, render_template, request

app = Flask(__name__)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/add_job')
def addJob():
    return render_template('jobs.html')

@app.route('/my_applications')
def myApplication():
    return render_template('applications.html')

if __name__ == '__main__':
    app.debug = True # server reloading
    app.run()