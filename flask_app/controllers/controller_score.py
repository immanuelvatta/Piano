from flask_app import app
import os
from flask import render_template, redirect, request, session, Response , flash
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
    # Check if a music sheet file was uploaded
    if 'music_sheet' not in request.files:
        flash('Please upload a music sheet.', 'err_score_music_sheet')
        return redirect('/score/new')
    # Get the uploaded music sheet from the request
    music_sheet = request.files['music_sheet']
    # Get the filename of the music sheet
    music_sheet_filename = music_sheet.filename
    
    # Validate the file extension
    allowed_extensions = {'pdf'}
    if '.' not in music_sheet_filename or music_sheet_filename.split('.')[-1].lower() not in allowed_extensions:
        flash("Invalid file format. Please upload a PDF file.", 'err_score_music_sheet')
        return redirect('/score/new')
    
    # Read the content of the music sheet
    music_sheet_content = music_sheet.read()
    # Define the path to save the PDF file temporarily
    pdf_file_path = f"temp/{music_sheet_filename}"
    # Check if the 'temp' directory exists, if it doesn't then creates it
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
    # Validate the score data using the 'score_validator' function
    if not Score.score_validator(data):
        # If the data is not valid, remove the temporary PDF file and redirect the user to the '/score/new' page
        os.remove(pdf_file_path)  # Remove the temporary PDF file
        return redirect('/score/new')
    # If the data is valid, create a new score using the 'create' function
    Score.create(data)
    # After successfully creating the score, redirect the user to the '/user/dashboard' page
    os.remove(pdf_file_path)  # Remove the temporary PDF file
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
        'Content-Type' : 'application/pdf',
        'Content-Disposition' : f'inline; filename="{score.name}.pdf"'
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

@app.route('/score/edit/<int:id>')
def score_edit(id):
    if not session:
        return redirect('/')
    user = User.get_one(session['email'])
    score = Score.get_one(id)
    return render_template('edit_score.html', user=user, score = score)


# controller_score.py

@app.route('/score/search', methods=['POST'])
def score_search():
    # Get the search query from the request form
    search_query = request.form['search_query']
    # Initialize an empty list to store the search results
    results = []
    # Check if the search query is not empty
    if search_query.strip():
        # If the search query is not empty, perform the search using the get_score_by_name method
        results = Score.get_score_by_name(search_query)
    # Get the number of search results
    num_results = len(results)
    return render_template('search_results.html', search_query=search_query, results=results, num_results = num_results )



@app.route('/score/updated/<int:id>', methods=["POST"])
def score_update(id):
    if not session:
        # If not logged in, redirect to the homepage
        return redirect('/')
    # Retrieve the existing score data from the database
    score = Score.get_one_score(id)
    if not score:
        # If score not found, return a 404 error
        return "Score not found", 404 
    # Get the uploaded music sheet from the request
    music_sheet = request.files['music_sheet']
    # Read the content of the music sheet
    music_sheet_content = music_sheet.read()
    # Define the path to save the PDF file temporarily
    pdf_file_path = f"temp/{music_sheet.filename}"
    # Check if the 'temp' directory exists, if it doesn't then creates it
    if not os.path.exists('temp'):
        os.makedirs('temp')
    # Save the music sheet content to a temporary PDF file
    with open(pdf_file_path, 'wb') as file:  # Use 'wb' mode to save the PDF file in binary mode
        file.write(music_sheet_content)
    # Create a dictionary 'data' with the form data and music sheet content
    data = {
        **request.form,
        'id': id,
        'music_sheet': music_sheet_content
    }
    # Validate the data before updating the score
    if not Score.score_validator(data):
        os.remove(pdf_file_path)
        return redirect(f'/score/edit/{id}')
    # Update the score in the database
    Score.update(data)
    # Remove the temporary PDF file after updating
    os.remove(pdf_file_path)
    # Redirect to the dashboard after successful update
    return redirect('/user/dashboard')



@app.route('/score/delete/<int:id>')
def score_delete(id):
    if not session:
        return redirect('/')
    Score.delete(id)
    return redirect('/user/dashboard')