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
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    flashcards = db.relationship('Flashcard', backref='user')
    decks = db.relationship('Deck', backref='user')
    study_frequency = db.relationship('StudyFrequency', backref='user')

#This class defines the Deck model for the database
class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    flashcards = db.relationship('Flashcard', backref='deck')
    study_frequency = db.relationship('StudyFrequency', backref='deck')

#These id value will be automatically set by the database software when a FC object
#is created.
class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    front = db.Column(db.String(10000))  # Will store Delta JSON
    back = db.Column(db.String(10000))   # Will store Delta JSON
    #This uses func to get the current date and time and save it to this variable
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    #This foreign key references the id from the User class
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'))
    study_frequency = db.relationship('StudyFrequency', backref='Flashcard')

    #This converts the flashcard object to a dictionary for transmission.
    def to_dict(self):
        return {
            'id': self.id,
            'front': self.front,
            'back': self.back,
            'date': self.date.isoformat()  # Convert datetime to ISO format string
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
