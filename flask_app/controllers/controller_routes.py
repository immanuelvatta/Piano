from flask_app import app

from flask import render_template
# from flask_app.models.model_user import User


# landing
@app.route('/')
def index():
    
    return render_template('login.html')