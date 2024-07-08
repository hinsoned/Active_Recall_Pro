# auth.py
# This file contains a Blueprint with routes to pages for login, logout, and signup

from flask import Blueprint, render_template

# Blueprints are used to define routes, error handlers, and other request-related 
# functions. It allows the views for the project to be defined in multiple files.
auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template("/login.html")

@auth.route('/logout')
def logout():
    return "<p>logout</p>"

@auth.route('/sign-up')
def sign_up():
    return render_template("/sign_up.html")