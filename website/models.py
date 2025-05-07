#models.py: This file contains the database models for the website.

#imports the database object from this package
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import json

#This class defines the User model for the database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    flashcards = db.relationship('Flashcard', foreign_keys='Flashcard.user_id', backref='user')
    decks = db.relationship('Deck', backref='user')
    study_frequency = db.relationship('StudyFrequency', backref='user')

    def get_recent_credits(self):
        """Calculate total credits earned in the last 30 days."""
        from datetime import datetime, timedelta
        from sqlalchemy import func
        
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        # Get all study credits from the last 30 days
        recent_credits = StudyCredit.query.filter(
            StudyCredit.created_at >= thirty_days_ago
        ).all()
        
        total_credits = 0
        for credit in recent_credits:
            # Get the credits for this user from the chain_credits JSON
            user_credits = credit.chain_credits.get(str(self.id), 0)
            total_credits += user_credits
            
        return round(total_credits, 2)  # Round to 2 decimal places

#This class defines the Deck model for the database
class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    flashcards = db.relationship('Flashcard', backref='deck')
    study_frequency = db.relationship('StudyFrequency', backref='deck')
    study_mode = db.Column(db.String(20), default='normal')  # 'normal' or 'sm2'

#These id value will be automatically set by the database software when a FC object
#is created.
class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    front = db.Column(db.String(10000))  # Will store Delta JSON
    back = db.Column(db.String(10000))   # Will store Delta JSON
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'))
    study_frequency = db.relationship('StudyFrequency', backref='Flashcard')

    # SM-2 specific fields
    repetitions = db.Column(db.Integer, default=0)  # n in SM-2
    ease_factor = db.Column(db.Float, default=2.5)  # EF in SM-2
    interval = db.Column(db.Integer, default=0)      # I in SM-2
    next_review_date = db.Column(db.DateTime(timezone=True), default=func.now())  # When to show next

    # Heritage system fields
    original_creator_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_original_creator'))
    heritage_chain = db.Column(db.JSON)  # Array of user IDs in order

    # Add relationship for original creator
    original_creator = db.relationship('User', foreign_keys=[original_creator_id], backref='created_cards')

    #This converts the flashcard object to a dictionary for transmission.
    def to_dict(self):
        return {
            'id': self.id,
            'front': self.front,
            'back': self.back,
            'date': self.date.isoformat(),  # Convert datetime to ISO format string
            'repetitions': self.repetitions,
            'ease_factor': self.ease_factor,
            'interval': self.interval,
            'next_review_date': self.next_review_date.isoformat() if self.next_review_date else None,
            'original_creator_id': self.original_creator_id,
            'heritage_chain': self.heritage_chain
        }

    # Return the content directly - Quill will handle conversion on frontend
    def get_front_html(self):
        return self.front

    def get_back_html(self):
        return self.back

#This class defines the StudyFrequency attached to each FlashCard
class StudyFrequency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    deck_id = db.Column(db.Integer, db.ForeignKey(Deck.id))
    flashcard_id = db.Column(db.Integer, db.ForeignKey(Flashcard.id))
    date = db.Column(db.String, default=func.current_date())
    frequency = db.Column(db.Integer)

# New model for tracking study credits
class StudyCredit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('flashcard.id'))
    studying_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    chain_credits = db.Column(db.JSON)  # Dictionary mapping user_id to credit amount
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
