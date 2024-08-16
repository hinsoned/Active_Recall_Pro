# views.py

#Imports Blueprint class from flask module. render_template allows you to render 
#templates from the folder templates. Flask is expecting a folder name templates by
#default.
from flask import Blueprint, render_template, request, flash, jsonify
# We use current-user to tell if user is logged in or anonymous
from flask_login import login_required, current_user
from .models import Flashcard , Deck
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
    decks = Deck.query.all()

    if request.method == 'POST':
        deckName = request.form.get('deckName')

        if not deckName:
            flash('That\'s not much of a deck!', category='error')
        else:
            #create the deck with the name and the user id
            new_deck = Deck(name=deckName, user_id=current_user.id)
            #add the deck do the database
            db.session.add(new_deck)
            db.session.commit()
            flash('Deck added!', category='success')

    return render_template("home.html", user=current_user, decks=decks)

    # if request.method == 'POST':
    #     front = request.form.get('front')
    #     back = request.form.get('back')

    #     if not front or not back:
    #         flash('That\'s not much of a flashcard!', category='error')
    #     else:
    #         #create the note with the text and the user id
    #         new_flashcard = Flashcard(front=front, back=back, user_id=current_user.id)
    #         #add the note do the database
    #         db.session.add(new_flashcard)
    #         db.session.commit()
    #         flash('Flashcard added!', category='success')
    # #This renders the template and also passes in the current_user variable.
    # #We can access the associated flashcards with current_user.flashcards
    # return render_template("home.html", user=current_user)

@views.route('/study', methods=['GET', 'POST'])
@login_required
def study():
    flashcards = [flashcard.to_dict() for flashcard in current_user.flashcards]
    return render_template("study.html", user=current_user, flashcards=flashcards)

@views.route('/deck/<int:deck_id>', methods=['GET', 'POST'])
def view_deck(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    flashcards = deck.flashcards  # Get all flashcards in this deck

    if request.method == 'POST':
        front = request.form.get('front')
        back = request.form.get('back')

        if not front or not back:
            flash('That\'s not much of a flashcard!', category='error')
        else:
            #create the note with the text and the user id
            new_flashcard = Flashcard(front=front, back=back,  deck_id=deck_id, user_id=current_user.id)
            #add the note do the database
            db.session.add(new_flashcard)
            db.session.commit()
            flash('Flashcard added!', category='success')
    return render_template('view_deck.html', deck=deck, flashcards=flashcards)

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