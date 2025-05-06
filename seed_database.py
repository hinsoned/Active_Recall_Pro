import json
from website import create_app, db
from website.models import User, Deck, Flashcard
from werkzeug.security import generate_password_hash

def seed_database():
    # Create the Flask application context
    app = create_app()
    
    with app.app_context():
        # Clear existing data (optional - be careful with this in production!)
        #db.drop_all()
        #db.create_all()
        
        # Load the seed data
        with open('seed_data.json', 'r') as f:
            data = json.load(f)
        
        # Process each user
        for user_data in data['users']:
            # Create the user
            user = User(
                email=user_data['email'],
                username=user_data['username'],
                first_name=user_data['first_name'],
                password=generate_password_hash(user_data['password'], method='pbkdf2:sha256')
            )
            db.session.add(user)
            db.session.flush()  # Get the user ID
            
            # Process each deck for this user
            for deck_data in user_data['decks']:
                deck = Deck(
                    name=deck_data['name'],
                    study_mode=deck_data['study_mode'],
                    user_id=user.id
                )
                db.session.add(deck)
                db.session.flush()  # Get the deck ID
                
                # Process each flashcard for this deck
                for card_data in deck_data['flashcards']:
                    flashcard = Flashcard(
                        front=card_data['front'],
                        back=card_data['back'],
                        user_id=user.id,
                        deck_id=deck.id
                    )
                    db.session.add(flashcard)
        
        # Commit all changes
        try:
            db.session.commit()
            print("Database seeded successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error seeding database: {e}")

if __name__ == '__main__':
    seed_database() 