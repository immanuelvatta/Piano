from flask_app import app
import os
from flask import render_template, redirect, request, session, Response
from flask_app.models.model_score import Score
from flask_app.models.model_user import User

@app.route('/score/new')
def score_new():
    if not session:
        return redirect('/')
    user = User.get_one(session['email'])
    
    return render_template('new_score.html', user =user)

@app.route('/score/create' , methods= ['POST'])
def score_create():
    
    # Get the uploaded music sheet from the request
    music_sheet = request.files['music_sheet']
    
    # Read the content of the music sheet
    music_sheet_content = music_sheet.read()
    # Define the path to save the PDF file temporarily
    pdf_file_path = f"temp/{music_sheet.filename}"
    
    # Check if the 'temp' directory exists, create it if not
    if not os.path.exists('temp'):
        os.makedirs('temp')
        
    # Save the music sheet content to a temporary PDF file
    with open(pdf_file_path, 'wb') as file:  # Use 'wb' mode to save the PDF file in binary mode
        file.write(music_sheet_content)
    
    # Create a dictionary 'data' with the form data and music sheet content
    data = {
        **request.form,
        'music_sheet': music_sheet_content
    }
    if not Score.score_validator(data):
        return redirect('/score/new')
    
    # If the data is valid, create a new score using the 'create' function
    Score.create(data)
    # After successfully creating the score, redirect the user to the '/user/dashboard' page
    return redirect('/user/dashboard')


@app.route('/score/display/<int:id>')
def score_display(id):
    
    # Retrieve the score with the given 'id' from the database
    score = Score.get_one_score(id)
    # Check if the score with the given 'id' exists
    if not score:
        # If the score is not found, return a "Score not found" message with 404 status code
        return "Score not found", 404
    
    # Prepare headers for the HTTP response to specify the PDF content type and filename
    headers = {
        'Content-Type': 'application/pdf',
        'Content-Disposition': f'inline; filename="{score.name}.pdf"'
    }
    # Create a response with the PDF content and headers
    response = Response(score.music_sheet, headers=headers)
    
    # Return the response to display the score PDF in the browser
    return response

@app.route('/score/view/<int:id>')
def score_view(id):
    # Check if the user is not authenticated (not in session)
    if not session:
        # If the user is not authenticated, redirect them to the home page ('/')
        return redirect('/')
    # Retrieve the user from the database using the email stored in the session
    user = User.get_one(session['email'])
    # Retrieve the score with the given 'id' from the database
    score = Score.get_one_score(id)
    # Check if the score with the given 'id' exists
    if not score:
        # If the score is not found, return a "Score not found" message with 404 status code
        return "Score not found", 404
    # Render the 'display_score.html' template with the user and score data
    return render_template('display_score.html', user=user, score=score)