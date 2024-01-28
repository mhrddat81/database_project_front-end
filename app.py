from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/trade_window')
def trade_window():
    return render_template('trade_window.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

if __name__ == '__main__':
    app.run(debug=True)
