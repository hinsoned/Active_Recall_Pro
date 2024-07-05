# auth.py

from flask import Blueprint

# Blueprints are used to define routes, error handlers, and other request-related 
# functions. It allows the views for the project to be defined in multiple files.
auth = Blueprint('auth', __name__)