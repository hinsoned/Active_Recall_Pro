# auth.py
# This file contains a Blueprint with routes to pages for login, logout, and signup

# The request object provides access to request data sent by a client to the server.
from flask import Blueprint, render_template, request, flash

# Blueprints are used to define routes, error handlers, and other request-related 
# functions. It allows the views for the project to be defined in multiple files.
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("/login.html")

@auth.route('/logout')
def logout():
    return "<p>logout</p>"

#Use methods associated with the request object to save form values to variables
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        #These if statements check the inputs for certain parameters
        if len(email) < 4:
            flash('Email must be greater than three characters.', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than one character.', category='error')
        elif password1 != password2:
            flash('The passwords do not match.', category='error')
        elif len(password1) < 7:
            flash('The password must have more than 6 characters.', category='error')
        else:
            # add the user to the database
            flash('Accoound created!', category='success')
            
    return render_template("/sign_up.html")