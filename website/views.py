# views.py

#Imports Blueprint class from flask module. render_template allows you to render 
#templates from the folder templates. Flask is expecting a folder name templates by
#default.
from flask import Blueprint, render_template, request, flash, jsonify
# We use current-user to tell if user is logged in or anonymous
from flask_login import login_required, current_user
from .models import Flashcard ,Deck, StudyFrequency
#import the database object
from . import db
import json
from datetime import datetime

# Blueprints are used to define routes, error handlers, and other request-related 
# functions. It allows the views for the project to be defined in multiple files.
views = Blueprint('views', __name__)

# This function will run when we go to '/' or the main page of the website
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    decks = Deck.query.all()

    if request.method == 'POST':
        #This converts the json data to a python dictionary
        data = request.get_json()
        #Now that we have a dictionary we can get the values we need
        deckName = data.get('deckName')

        if not deckName:
            return jsonify({'success': False, 'message': 'Deck name is required'}), 400

        #create the deck with the name and the user id
        new_deck = Deck(name=deckName, user_id=current_user.id)
        #add the deck do the database
        db.session.add(new_deck)
        db.session.commit()
        return jsonify({'success': True, 'deck': {'id': new_deck.id, 'name': new_deck.name}}), 200

    return render_template("home.html", user=current_user, decks=decks)

# the route for studying a deck
@views.route('/study/<int:deck_id>', methods=['GET', 'POST'])
@login_required
def study(deck_id):
    if request.method == 'POST':
        data = request.get_json()
        flashcard_id = data.get('flashcard_id')

        if not flashcard_id:
            return jsonify({'success': False, 'message': 'Something happened in Front End'}), 400
        
        cur_date = datetime.today().strftime('%Y-%m-%d')

        study_instance = StudyFrequency.query.filter_by(user_id=current_user.id, deck_id=deck_id, flashcard_id=flashcard_id, date=cur_date)

        if (not study_instance.first()):
            new_study_frequency = StudyFrequency(user_id=current_user.id, deck_id=deck_id, flashcard_id=flashcard_id, frequency=1)
            db.session.add(new_study_frequency)
        else:
            study_instance.update(
                { StudyFrequency.frequency : StudyFrequency.frequency + 1 } ,
                synchronize_session=False
            )

        db.session.commit()

        return jsonify({'success': True}), 200


    deck = Deck.query.get_or_404(deck_id)
    flashcards = [flashcard.to_dict() for flashcard in deck.flashcards]

    return render_template("study.html", user=current_user, flashcards=flashcards, deck=deck, deck_id=deck_id)

# the route for viewing a deck
@views.route('/deck/<int:deck_id>', methods=['GET', 'POST'])
@login_required
def view_deck(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    flashcards = deck.flashcards  # Get all flashcards in this deck

    if request.method == 'POST':
        #This converts the json data to a python dictionary
        data = request.get_json()
        #Now that we have a dictionary we can get the values we need
        front = data.get('front')
        back = data.get('back')

        if not front or not back:
            return jsonify({'success': False, 'message': 'Both front and back are required'}), 400

        #create the note with the text and the user id
        new_flashcard = Flashcard(front=front, back=back,  deck_id=deck_id, user_id=current_user.id)
        #add the note do the database
        db.session.add(new_flashcard)
        db.session.commit()

        #This returns a json object with the success key set to true and the new flashcard information in json form 
        return jsonify({'success': True, 'flashcard': {'id': new_flashcard.id, 'front': new_flashcard.front, 'back': new_flashcard.back}})

    return render_template('view_deck.html', deck=deck, deck_id=deck_id, flashcards=flashcards)

# the route for editing a flashcard
@views.route('/edit-flashcard/<int:flashcard_id>', methods=['GET', 'POST'])
@login_required
def edit_flashcard(flashcard_id):
    flashcard = Flashcard.query.get_or_404(flashcard_id)

    if request.method == 'POST':
        data = request.get_json()
        front = data.get('front')
        back = data.get('back')

        if not front or not back:
            return jsonify({'success': False, 'message': 'Both front and back are required'}), 400

        flashcard.front = front
        flashcard.back = back
        db.session.commit()

        return jsonify({'success': True, 'flashcard': {'id': flashcard.id, 'front': flashcard.front, 'back': flashcard.back}})

    return render_template('edit_card.html', flashcard=flashcard)

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

# This is the backend for Heat Map
@views.route('/heatmap', methods=['GET', 'POST'])
@login_required
def heat_map():

    return render_template("heat_map.html")