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

@views.route('/study/<int:deck_id>', methods=['GET', 'POST'])
@login_required
def study(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    flashcards = [flashcard.to_dict() for flashcard in deck.flashcards]
    return render_template("study.html", user=current_user, flashcards=flashcards, deck=deck)

@views.route('/deck/<int:deck_id>', methods=['GET', 'POST'])
@login_required
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
    return render_template('view_deck.html', deck=deck, deck_id=deck_id, flashcards=flashcards)

@views.route('/delete-flashcard', methods=['POST'])
@login_required
def delete_flashcard():
    #This converts the json data to a python dictionary
    flashcard_data = json.loads(request.data)
    #This gets the flashcard id from the dictionary. The key is 'flashcardId' and the value is the acutal flashcard id
    flashcard_id = flashcard_data['flashcardId']
    #This gets the flashcard object using the flashcard id
    flashcard = Flashcard.query.get(flashcard_id)

    #This checks if the current user is the user who created the flashcard
    if flashcard and flashcard.user_id == current_user.id:
            db.session.delete(flashcard)
            db.session.commit()
            #This returns a json object with the deleted key set to true
            return jsonify({ 'deleted': True })
    
    return jsonify({ 'deleted': False })

# This works the same as the delete-flashcard function but also deletes the flashcards in the deck using the deck_id
@views.route('/delete-deck', methods=['POST'])
@login_required
def delete_deck():
    deck_data = json.loads(request.data)
    deck_id = deck_data['deckId']
    deck = Deck.query.get(deck_id)

    if deck and deck.user_id == current_user.id:
        # Delete all flashcards associated with the deck
        Flashcard.query.filter_by(deck_id=deck_id).delete()
        db.session.delete(deck)
        db.session.commit()
        return jsonify({'success': True})

    return jsonify({'success': False}), 400
