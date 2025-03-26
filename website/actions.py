#actions.py
#This is for non-rendering endpoints. It cleans up the views.py file.

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from . import db
from .models import Flashcard, Deck
import json

actions = Blueprint('actions', __name__)

@actions.route('/delete-flashcard', methods=['POST'])
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
@actions.route('/delete-deck', methods=['POST'])
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

#Sets up the initial study page
@actions.route('/study/<int:deck_id>/config', methods=['GET'])
@login_required
def study_config(deck_id):
    print(f"Deck ID: {deck_id}")
    deck = Deck.query.get_or_404(deck_id)
    deck_length = len(deck.flashcards)
    return jsonify({"deck_id": deck_id, "deck_length": deck_length})

#returns a dictionary object that is turned in to json by jsonify
@actions.route('/study/<int:deck_id>/<int:index>', methods=['GET'])
@login_required
def get_flashcard(deck_id, index):
    deck = Deck.query.get_or_404(deck_id)
    flashcard = deck.flashcards[index].to_dict()
    return jsonify({'success': True, 'flashcard': flashcard}), 200