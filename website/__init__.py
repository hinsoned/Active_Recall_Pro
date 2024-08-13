# __init__.pymakes the 'website' directory a python package which makes imports easier. 
# The file also details the create_app() function which is a application factory function which includes 
# registering blueprints, creating an instance of login manager, and linking the app to the database.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

# This is the "application factory" that creates a flask instance.
def create_app():
        app = Flask(__name__)

        app.config['SECRET_KEY'] = 'Brooklyn Nets'
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), DB_NAME)}'

        # Links app to db object
        db.init_app(app)

        # Import blueperint objects and registers them.
        from .views import views
        from .auth import auth
        app.register_blueprint(views, url_prefix='/')
        app.register_blueprint(auth, url_prefix='/')

        # imports User model
        from .models import User
        from .models import Flashcard

        #create the database based on the models
        with app.app_context():
                db.create_all()

        #create an instance of LoginManager and connect it to the app
        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.init_app(app)

        #this finds the primary key for the user (the id)
        @login_manager.user_loader
        def load_user(id):
                return User.query.get(int(id))

        return app