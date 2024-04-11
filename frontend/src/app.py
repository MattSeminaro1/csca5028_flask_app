#!/usr/bin/env python3

from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

# Define routes and view functions
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/select/<choice>')
def select(choice):
    if choice == 'pitching':
        return redirect(url_for('pitching'))
    elif choice == 'batting':
        return redirect(url_for('batting'))
    else:
        return "Invalid choice"

@app.route('/pitching')
def pitching():
    # Code for pitching endpoint
    return "Pitching data"

@app.route('/batting')
def batting():
    # Code for batting endpoint
    return "Batting data"

if __name__ == '__main__':
    app.run(debug=True)