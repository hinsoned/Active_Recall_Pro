#actions.py
#This is for non-rendering endpoints. It cleans up the views.py file.

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from . import db
from .models import Flashcard, Deck, StudyCredit
import json
from datetime import datetime, timedelta

actions = Blueprint('actions', __name__)

def distribute_study_credit(card, studying_user_id):
    """Distribute study credits to users in the heritage chain."""
    # Get the heritage chain, defaulting to just the original creator if none exists
    heritage_chain = card.heritage_chain or [card.original_creator_id]
    
    # Calculate credits for each user in the chain
    # Original creator gets 50%, last 3 users in chain split remaining 50%
    chain_credits = {}
    
    # Original creator gets 50%
    chain_credits[card.original_creator_id] = 0.5
    
    # Last 3 users in chain split remaining 50%
    recent_users = heritage_chain[-3:] if len(heritage_chain) > 1 else []
    if recent_users:
        remaining_credit = 0.5 / len(recent_users)
        for user_id in recent_users:
            if user_id != card.original_creator_id:  # Don't double-count original creator
                chain_credits[user_id] = remaining_credit
    
    # Create study credit record
    study_credit = StudyCredit(
        card_id=card.id,
        studying_user_id=studying_user_id,
        chain_credits=chain_credits
    )
    db.session.add(study_credit)

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
    deck = Deck.query.get_or_404(deck_id)
    deck_length = len(deck.flashcards)
    return jsonify({
        "deck_id": deck_id, 
        "deck_length": deck_length,
        "study_mode": deck.study_mode
    })

#returns a dictionary object that is turned in to json by jsonify
@actions.route('/study/<int:deck_id>/<int:index>', methods=['GET'])
@login_required
def get_flashcard(deck_id, index):
    deck = Deck.query.get_or_404(deck_id)
    flashcard = deck.flashcards[index].to_dict()
    return jsonify({'success': True, 'flashcard': flashcard}), 200

@actions.route('/api/deck/<int:deck_id>/flashcards', methods=['GET'])
def get_deck_flashcards(deck_id):
    #deck = Deck.query.get_or_404(deck_id)
    flashcards = Flashcard.query.filter_by(deck_id=deck_id).all()
    
    return jsonify({
        'success': True,
        'flashcards': [flashcard.to_dict() for flashcard in flashcards]
    })

@actions.route('/study/<int:deck_id>/rate', methods=['POST'])
@login_required
def rate_flashcard(deck_id):
    data = request.get_json()
    flashcard_id = data.get('flashcard_id')
    rating = data.get('rating')

    if not flashcard_id or rating is None:
        return jsonify({'success': False, 'message': 'Missing flashcard_id or rating'}), 400

    flashcard = Flashcard.query.get(flashcard_id)
    if not flashcard:
        return jsonify({'success': False, 'message': 'Flashcard not found'}), 404

    # SM-2 Algorithm
    if rating >= 3:  # Correct response
        if flashcard.repetitions == 0:
            flashcard.interval = 1  # 5 minutes
        elif flashcard.repetitions == 1:
            flashcard.interval = 6  # 30 minutes
        else:
            flashcard.interval = int(flashcard.interval * flashcard.ease_factor)
        
        flashcard.repetitions += 1
        flashcard.ease_factor = max(1.3, flashcard.ease_factor + (0.1 - (5 - rating) * (0.08 + (5 - rating) * 0.02)))
    else:  # Incorrect response
        flashcard.repetitions = 0
        flashcard.interval = 1  # 5 minutes
        flashcard.ease_factor = max(1.3, flashcard.ease_factor - 0.2)

    # Update next review date using 5-minute intervals
    flashcard.next_review_date = datetime.utcnow() + timedelta(minutes=flashcard.interval * 5)
    
    # Distribute study credits
    distribute_study_credit(flashcard, current_user.id)
    
    db.session.commit()

    return jsonify({
        'success': True,
        'card': flashcard.to_dict()
    })

# SM-2 algorithm: This function gets all the cards due for review in a deck for the SM-2 algorithm
@actions.route("/study/<int:deck_id>/due", methods=["GET"])
def get_due_cards(deck_id):
    """Get all cards due for review in a deck"""
    try:
        # Get the deck
        deck = Deck.query.get(deck_id)
        if not deck:
            return jsonify({"success": False, "message": "Deck not found"}), 404

        # Get current time in UTC
        now = datetime.utcnow()

        # Get all cards that are due for review
        due_cards = Flashcard.query.filter(
            Flashcard.deck_id == deck_id,
            Flashcard.next_review_date <= now
        ).order_by(Flashcard.next_review_date.asc()).all()

        # If no cards are due, get new cards (cards that have never been reviewed)
        if not due_cards:
            due_cards = Flashcard.query.filter(
                Flashcard.deck_id == deck_id,
                Flashcard.next_review_date == None
            ).all()

        # Convert cards to dictionary format
        cards_data = [{
            "id": card.id,
            "front": card.front,
            "back": card.back,
            "repetitions": card.repetitions,
            "ease_factor": card.ease_factor,
            "interval": card.interval,
            "next_review_date": card.next_review_date.isoformat() if card.next_review_date else None
        } for card in due_cards]

        # Return the cards dictionary as a json object
        return jsonify({
            "success": True,
            "cards": cards_data
        })

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@actions.route('/update-study-mode/<int:deck_id>', methods=['POST'])
@login_required
def update_study_mode(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    if deck.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    data = request.get_json()
    study_mode = data.get('study_mode')
    
    if study_mode not in ['normal', 'sm2']:
        return jsonify({'success': False, 'message': 'Invalid study mode'}), 400
    
    deck.study_mode = study_mode
    db.session.commit()
    
    return jsonify({'success': True, 'study_mode': study_mode}), 200

@actions.route('/api/user/decks', methods=['POST'])
@login_required
def get_user_decks():
    data = request.get_json()
    current_deck_id = data.get('current_deck_id')
    
    query = Deck.query.filter_by(user_id=current_user.id)
    if current_deck_id:
        query = query.filter(Deck.id != current_deck_id)
    
    decks = query.all()
    return jsonify({
        'success': True,
        'decks': [{'id': deck.id, 'name': deck.name} for deck in decks]
    })

@actions.route('/api/move-card', methods=['POST'])
@login_required
def move_card():
    data = request.get_json()
    flashcard_id = data.get('flashcardId')
    target_deck_id = data.get('targetDeckId')
    
    if not flashcard_id or not target_deck_id:
        return jsonify({'success': False, 'message': 'Missing flashcard ID or target deck ID'}), 400
    
    flashcard = Flashcard.query.get(flashcard_id)
    target_deck = Deck.query.get(target_deck_id)
    
    if not flashcard or not target_deck:
        return jsonify({'success': False, 'message': 'Flashcard or deck not found'}), 404
    
    if flashcard.user_id != current_user.id or target_deck.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    flashcard.deck_id = target_deck_id
    db.session.commit()
    
    return jsonify({'success': True})

@actions.route('/api/deck/<int:deck_id>/copy', methods=['POST'])
@login_required
def copy_deck(deck_id):
    # Get the original deck
    original_deck = Deck.query.get_or_404(deck_id)
    
    # Create a new deck for the current user
    new_deck = Deck(
        name=original_deck.name,
        user_id=current_user.id,
        study_mode=original_deck.study_mode
    )
    db.session.add(new_deck)
    db.session.flush()  # This gets us the new deck's ID
    
    # Copy all flashcards from the original deck
    for flashcard in original_deck.flashcards:
        # Get the original heritage chain or create a new one
        heritage_chain = flashcard.heritage_chain or [flashcard.original_creator_id]
        
        # Add current user to the heritage chain if not already present
        if current_user.id not in heritage_chain:
            heritage_chain.append(current_user.id)
        
        new_flashcard = Flashcard(
            front=flashcard.front,
            back=flashcard.back,
            deck_id=new_deck.id,
            user_id=current_user.id,
            original_creator_id=flashcard.original_creator_id,  # Preserve original creator
            heritage_chain=heritage_chain,  # Updated heritage chain
            repetitions=0,
            ease_factor=2.5,
            interval=0,
            next_review_date=datetime.utcnow()
        )
        db.session.add(new_flashcard)
    
    db.session.commit()
    return jsonify({'success': True, 'message': 'Deck copied successfully'})
