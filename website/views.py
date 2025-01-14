# views.py

#Imports Blueprint class from flask module. render_template allows you to render 
#templates from the folder templates. Flask is expecting a folder name templates by
#default.
from flask import Blueprint, render_template, request, flash, jsonify
# We use current-user to tell if user is logged in or anonymous
from flask_login import login_required, current_user
from .models import Flashcard ,Deck, StudyFrequency
from . import db
import json
from datetime import datetime

# Blueprints are used to define routes, error handlers, and other request-related 
# functions. It allows the views for the project to be defined in multiple files.
views = Blueprint('views', __name__)

# This function will run when we go to '/' or the main page of the website
@views.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
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
    else:
        return render_template("landing_page.html")

# The route for studying a deck
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

    return render_template("study.html", user=current_user, deck=deck, deck_id=deck_id, deck_length=len(flashcards))

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

# This is the backend for Heat Map. It reads the StudyFrequency table based on the user and passes the date and freq to the front end.
@views.route('/heatmap/<int:user_id>', methods=['GET', 'POST'])
@login_required
def heat_map(user_id):  
    user_heat = StudyFrequency.query.filter_by(user_id = user_id).all()
    heat_dict = {}
    for heat in user_heat:
        date = heat.date
        freq = heat.frequency

        if date not in heat_dict:
            heat_dict[date] = freq
        else:
            heat_dict[date] += freq

    return render_template("heat_map.html", heat_dict=heat_dict)