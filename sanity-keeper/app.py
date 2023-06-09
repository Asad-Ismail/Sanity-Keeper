from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your-secret-key' # change this!

# For demonstration purposes we'll use a dictionary instead of a database
users = {}

@app.route("/")
def home():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username not in users:
            users[username] = generate_password_hash(password)
            return redirect(url_for('login'))
        else:
            return 'Username already exists!'
    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username not in users:
            return 'Username does not exist!'
        else:
            if check_password_hash(users[username], password):
                session['username'] = username
                return redirect(url_for('home'))
            else:
                return 'Incorrect password!'
    return render_template('login.html')

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)

