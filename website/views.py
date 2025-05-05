# views.py

#Imports Blueprint class from flask module. render_template allows you to render 
#templates from the folder templates. Flask is expecting a folder name templates by
#default.
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
# We use current-user to tell if user is logged in or anonymous
from flask_login import login_required, current_user
from .models import Flashcard ,Deck, StudyFrequency, User
from . import db
import json
from datetime import datetime
#import bleach

# Blueprints are used to define routes, error handlers, and other request-related 
# functions. It allows the views for the project to be defined in multiple files.
views = Blueprint('views', __name__)

# This function will run when we go to '/' or the main page of the website
@views.route('/', methods=['GET'])
def home():
    if current_user.is_authenticated:
        return render_template("home.html", user=current_user)
    else:
        return render_template("landing_page.html")

# Profile page showing user's decks
@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    # Only fetch decks belonging to the current user
    decks = Deck.query.filter_by(user_id=current_user.id).all()

    if request.method == 'POST':
        data = request.get_json()
        deckName = data.get('deckName')
        studyMode = data.get('studyMode', 'normal')  # Default to normal if not specified

        if not deckName or not deckName.strip():
            return jsonify({'success': False, 'message': 'Deck name is required'}), 400

        #create the deck with the name, user id, and study mode
        new_deck = Deck(name=deckName, user_id=current_user.id, study_mode=studyMode)
        #add the deck to the database
        db.session.add(new_deck)
        db.session.commit()
        return jsonify({'success': True, 'deck': {'id': new_deck.id, 'name': new_deck.name, 'study_mode': new_deck.study_mode}}), 200

    return render_template("profile.html", user=current_user, decks=decks)

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

    return render_template("study.html", user=current_user, deck=deck)

# the route for viewing a deck
@views.route('/deck/<int:deck_id>', methods=['GET', 'POST'])
@login_required
def view_deck(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    print(f"Deck data: {deck.name}, User: {deck.user.username}, Flashcards: {len(deck.flashcards)}")
    
    # If the user is not the owner of the deck, redirect to public view
    if deck.user_id != current_user.id:
        return render_template('view_public_deck.html',
            deck_id=deck.id,
            deck_name=deck.name,
            study_mode=deck.study_mode,
            deck=deck)
    
    if request.method == 'POST':
        data = request.get_json()
        front = data.get('front')
        back = data.get('back')

        if not front or not back:
            return jsonify({'success': False, 'message': 'Both front and back are required'}), 400

        try:
            # Validate that the content is valid JSON
            json.loads(front)
            json.loads(back)
        except json.JSONDecodeError:
            return jsonify({'success': False, 'message': 'Invalid content format'}), 400

        #create the flashcard with the text, user id, and SM-2 defaults
        new_flashcard = Flashcard(
            front=front, 
            back=back, 
            deck_id=deck_id, 
            user_id=current_user.id,
            repetitions=0,
            ease_factor=2.5,
            interval=0,
            next_review_date=datetime.utcnow()
        )
        #add the flashcard to the database
        db.session.add(new_flashcard)
        db.session.commit()

        #This returns a json object with the success key set to true and the new flashcard information in json form 
        return jsonify({'success': True, 'flashcard': new_flashcard.to_dict()})

    return render_template('view_deck.html', 
        deck_id=deck.id,
        deck_name=deck.name,
        study_mode=deck.study_mode,
        deck=deck)

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

        try:
            # Validate that the content is valid JSON
            json.loads(front)
            json.loads(back)
        except json.JSONDecodeError:
            return jsonify({'success': False, 'message': 'Invalid content format'}), 400

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

@views.route('/profile/<int:user_id>', methods=['GET'])
@login_required
def view_profile(user_id):
    # Get the user whose profile we're viewing
    viewed_user = User.query.get_or_404(user_id)
    
    # Don't allow users to view their own profile through this route
    if viewed_user.id == current_user.id:
        return redirect(url_for('views.profile'))
    
    return render_template('view_profile.html', viewed_user=viewed_user)