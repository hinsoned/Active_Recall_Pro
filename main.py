#!/usr/bin/env python3
# main.py
# This page launches the app by importing the create_app function from somewhere in the website package, 
# __init__.py specifically, and running it.
import sys
print(sys.path)

from website import create_app
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False) #Change debug to false when website is live!!!