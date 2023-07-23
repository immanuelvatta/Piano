from flask_app import app

from flask import render_template
# from flask_app.models.model_user import User


# landing
@app.route('/')
def index():
    
    # user = None # can replace None with "" or False, or None
    # if session:
    #     return redirect('/user/success')
    #     user = User.get_one({'id': session['user_id']})
    #     session['user_id'] = user.id
    return render_template('login.html')