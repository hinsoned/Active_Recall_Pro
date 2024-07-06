# views.py

#Imports Bluepring class from flask module
from flask import Blueprint

# Blueprints are used to define routes, error handlers, and other request-related 
# functions. It allows the views for the project to be defined in multiple files.
views = Blueprint('views', __name__)

# This function will run when we go to '/' or the main page of the website
@views.route('/')
def home():
    return "<h1> Test</h1>"