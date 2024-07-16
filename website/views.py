# views.py

#Imports Blueprint class from flask module. render_template allows you to render 
#templates from the folder templates. Flask is expecting a folder name templates by
#default.
from flask import Blueprint, render_template
# We use current-user to tell if user is logged in or anonymous
from flask_login import login_required, current_user

# Blueprints are used to define routes, error handlers, and other request-related 
# functions. It allows the views for the project to be defined in multiple files.
views = Blueprint('views', __name__)

# This function will run when we go to '/' or the main page of the website
@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)