# __init__.py
from flask import Flask

# This is a factory function that creates a flask instance.
# '__name__' is a special variable that indicates the current module ( .py file)
def create_app():
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'Brooklyn Nets'

        return app