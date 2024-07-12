# __init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import os

# db is the instance of SQLAlchemy we are using. This object is the bridge between
# the flask app and the database.
db = SQLAlchemy()

DB_NAME = "database.db"

#These are various attempts to make the database file appear that may have been
#unncessary.
#basedir = os.path.abspath(os.path.dirname(__file__))
#DB_NAME = "database.db"
#DB_PATH = os.path.join(basedir, DB_NAME)
#DB_PATH = path.join(path.dirname(__file__), DB_NAME)

# This is a factory function that creates a flask instance.
# '__name__' is a special variable that indicates the current module ( .py file)
def create_app():
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'Brooklyn Nets'
        # This tells flask where to store the database file in the website folder
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), DB_NAME)}'
        # This defines the connection between the database created above and the app.
        # After this, db can interact with the SQLite database specified in 
        # SQLALCHEMY_DATABASE_URI.
        db.init_app(app)

        from .views import views
        from .auth import auth

        #These make the path to access the routes in the blueprints available.
        #The url prefix for both views in both will be '/'
        app.register_blueprint(views, url_prefix='/')
        app.register_blueprint(auth, url_prefix='/')

        #The . indicates the current package. This registers these models with SQLAlchemy.
        # SQLAlchemy keeps track of all models that are defined before you call db.create_all(app=app).
        from .models import User, Note

        with app.app_context():
                db.create_all()

        return app