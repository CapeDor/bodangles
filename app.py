from flask import Flask, flash, render_template, request, url_for
import os
app = Flask(__name__)
app.secret_key = os.urandom(12)

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['password'] != 'admin':
            error = 'Invalid credentials'
        else:
            flash('You were succesfully logged in')
            return render_template('data.html')
    return render_template('login.html', error=error)
