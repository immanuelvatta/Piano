from flask_app import app, bcrypt

from flask import render_template, redirect, request, session

#TODO change this
from flask_app.models.model_user import User
from flask_app.models.model_score import Score

# '/user/new' -> display the route with the form
@app.route('/user/new')
def user_new():
    return render_template('register.html')

# '/user/create' -> process the form from above
@app.route('/user/create', methods=['POST'])
def user_create():
    
    
    data = {
        **request.form
    }
    if not User.validator(data):
        return redirect('/user/new')
    
    
    hash_pw = bcrypt.generate_password_hash(data['password'])
    print(data['password'])
    data['password'] = hash_pw
    print(data['password'])
    #do the creating
    User.create(data)
    # session['user_id'] = user_id
    session['email'] = request.form['email']
    
    
    #use session 
    return redirect('/user/dashboard')

@app.route('/user/login', methods=['POST'])
def user_login():
    is_valid = User.validator_login(request.form)
    if is_valid == False:
        return redirect('/')
    else:
        session['email'] = is_valid
    
    return redirect('/user/dashboard')

@app.route('/user/dashboard')
def success():
    if not session:
        return redirect('/')
    user = User.get_one(session['email'])

    scores = Score.get_all()
    return render_template("dashboard.html", user= user, scores = scores)


@app.route('/user/logout')
def logout():
    session.clear()
    return redirect('/')



# '/user/<int:id>' -> display the user's info -> Show
# '/user/<int:id>/edit' -> display the user's info in a form so that they can edit it
# '/user/<int:id>/update' -> process the edit form
# '/user/<int:id>/delete' -> delete the user at that id
