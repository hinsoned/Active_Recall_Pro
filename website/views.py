# views.py

#Imports Blueprint class from flask module. render_template allows you to render 
#templates from the folder templates. Flask is expecting a folder name templates by
#default.
from flask import Blueprint, render_template, request, flash, jsonify
# We use current-user to tell if user is logged in or anonymous
from flask_login import login_required, current_user
from .models import Flashcard
#import the database object
from . import db
import json

# Blueprints are used to define routes, error handlers, and other request-related 
# functions. It allows the views for the project to be defined in multiple files.
views = Blueprint('views', __name__)

# This function will run when we go to '/' or the main page of the website
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        #note = request.form.get('note')
        front = request.form.get('front')
        back = request.form.get('back')

        if not front or not back:
            flash('That\'s not much of a flashcard!', category='error')
        else:
            #create the note with the text and the user id
            new_flashcard = Flashcard(front=front, back=back, user_id=current_user.id)
            #add the note do the database
            db.session.add(new_flashcard)
            db.session.commit()
            flash('Flashcard added!', category='success')
    #This renders the template and also passes in the current_user variable.
    #We can access the associated flashcards with current_user.flashcards
    return render_template("home.html", user=current_user)

@views.route('/study', methods=['GET', 'POST'])
@login_required
def study():
    flashcards = [flashcard.to_dict() for flashcard in current_user.flashcards]
    return render_template("study.html", user=current_user, flashcards=flashcards)

@views.route('/delete-flashcard', methods=['POST'])
def delete_flashcard():
    flashcard = json.loads(request.data)
    flashcardId = flashcard['flashcardId']
    flashcard = Flashcard.query.get(flashcardId)
    if flashcard: 
        if flashcard.user_id == current_user.id:
            db.session.delete(flashcard)
            db.session.commit()
            
    return jsonify({})