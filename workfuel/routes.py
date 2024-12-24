from flask import render_template
from workfuel import app


@app.route('/')
def main_page():
    return render_template('main_page.html')
