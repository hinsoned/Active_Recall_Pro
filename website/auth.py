# auth.py
# This file contains a Blueprint with routes to pages for login, logout, and signup

# The request object provides access to request data sent by a client to the server.
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
#the current-user import allows access to info about current user
from flask_login import login_user, login_required, logout_user, current_user

# Blueprints are used to define routes, error handlers, and other request-related 
# functions. It allows the views for the project to be defined in multiple files.
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        #this returns the first result in the db where the user email matches the email
        #from the form. There should be one of zero results.
        user = User.query.filter_by(email=email).first()
        #This only runs if the query returned a user at all
        if user:
            #user.password is the password for the user we just looked up. password
            # is the password from the form. This compares them.
            if check_password_hash(user.password, password):
                flash('You are logged in!', category='success')
                #This is what actually logs in the user.
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password', category='error')
        else:
            flash('No user with that email', category='error')
                
    return render_template("/login.html", user=current_user)

@auth.route('/logout')
#this just means that you can not get to the logout page without being logged in
def logout():
    logout_user()
    return render_template("landing_page.html")

#Use methods associated with the request object to save form values to variables
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        #assigns values from form to variables
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #check if the user exists already
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        #These if statements check the inputs for certain parameters
        elif len(email) < 4:
            flash('Email must be greater than three characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than one character.', category='error')
        elif password1 != password2:
            flash('The passwords do not match.', category='error')
        elif len(password1) < 7:
            flash('The password must have more than 6 characters.', category='error')
        else:
            #Add the user to the database. Takes values in variables above and 
            #passes them to a user object in database.
            new_user = User(email= email, first_name=first_name, password=generate_password_hash(password1, method= 'pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
            
    return render_template("/sign_up.html", user=current_user)