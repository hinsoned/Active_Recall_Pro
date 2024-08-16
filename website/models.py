#models.py: This file contains the database models for the website.

#imports the database object from this package
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#This class defines the User model for the database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    flashcards = db.relationship('Flashcard', backref='user')
    decks = db.relationship('Deck', backref='user')

#This class defines the Deck model for the database
class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    flashcards = db.relationship('Flashcard', backref='deck')

#These id value will be automatically set by the database software when a FC object
#is created.
class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    front = db.Column(db.String(10000))
    back = db.Column(db.String(10000))
    #This uses func to get the current date and time and save it to this variable
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    #This foreign key references the id from the User class
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'))

    #This converts the flashcard object to a dictionary for transmission.
    def to_dict(self):
        return {
            'id': self.id,
            'front': self.front,
            'back': self.back,
            'date': self.date.isoformat()  # Convert datetime to ISO format string
        }
