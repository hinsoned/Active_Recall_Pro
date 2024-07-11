# Active_Recall_Pro (This is a stand-in name)
 A flashcard web app project.
## GOAL:
The immediate goal is to create a flash card application that allows users to log in, create multimedia flash cards, edit flash cards, delete flash cards, and study flash cards. The long term plan is to add a social feature that would allow users to make decks public (so that they may be seen and studied by other users) or private (so that only the creator can see the deck and its cards). I also hope to add a version control feature similar to Git for flashcard decks. This would allow users to copy a public deck to their profile and modify it, or to collaborate on decks using a Git-like branch structure. Tracking stats on who creates popular decks (meaning decks that are studied, copied, and branched often) could allow a ranking or reward system to benefit power-users. Features such as a heat map for studying similar to anki or GitHub, and time view (a view of a deck arranged for studying based on the week of a class one is in) are also possible. Most importantly, users own their cards and they will be saved to the user’s machine to be synced to the site later.

Not that this code will be HEAVILY commented as I am using it as a learning tool and hop too colaborate on later features.

## TODO:
1. Create initial notes app following tutorial: https://www.youtube.com/watch?v=dam0GPOAvVI
    - Figure out pyache issue. What is it?
    - Understand secret key from __init__.py
    - Understand @ symbol in relation to routes.
2. Convert Notes to flashcards
3. Enable Images in flashcards
4. Enable flashcards to be organized in to decks
5. Create and admin area: All users, decks, stats are visible
6. Enable spaced repetition algorithm
7. Improve Bootstrap UI
8. Add heat Map feature
9. Add collaborative/public decks
10. Add Deck copy feature: Cards will be visible before copy and download.
11. Add deck branch feature
12. Add school specific feature. Decks can be made for certain classes at specific schools with both topic view and time view for the decks.
13. Create desktop app (99designs??)
14. Create mobile app (99designs??)

## RELEVANT TUTORIALS:
1. To follow for creation of a notes App. Includes information on file structure, use of Flask,  and SQL integration https://www.youtube.com/watch?v=dam0GPOAvVI
2. For installation of python, PIP, and general Flask,https://www.youtube.com/watch?v=Z1RJmh_OqeA
3. Blueprints in flask https://www.youtube.com/watch?v=WteIH6J9v64
3. Bootstrap tutorial long: https://www.youtube.com/watch?v=-qfEOE4vtxE
4. Bootstrap tutorial short: https://www.youtube.com/watch?v=eow125xV5-c
5. Admin area https://www.youtube.com/watch?v=WqHtmz8Ibn8
6. Tkinter https://www.youtube.com/watch?v=Pd3XoLSQ5wg

## RELEVANT LINKS:
1. Bootstrap. open source CSS Framework used in the main tutorial:https://www.youtube.com/watch?v=eow125xV5-c Home page: https://getbootstrap.com/
2. Flask-Admin https://flask-admin.readthedocs.io/en/latest/

## NOTES
- __init__.py :It tells python that the directory this file is in is a package. You can import modules from files in this package to other files using import statments and more. It facilitates the reuse of components within the package. https://www.youtube.com/watch?v=mWaMSGwiSB0

- Blueprints: Effectively this allows you to create url routes that return different things that can then be used in a different file using the .register_blueprint( ) function. https://www.youtube.com/watch?v=_LMiUOYDxzE&t=24s

- Jinja2: This is a templating language that allows you to put some python in html files. It makes use of {%%} to create blocks that can be overwritten in a base file by elements of other files. This isincluded with the flask install. https://www.youtube.com/watch?v=4yaG-jFfePc For documentation see: https://jinja.palletsprojects.com/en/3.1.x/

- render_template: When you call render_template('home.html'), Flask looks for the home.html file in the templates directory. By default Flask expects the templates to be located in a directory named templates within your application's directory structure.

- request (the flask object): The request object is used to handle incoming request data. It provides access to the request data sent by the client, such as form data, query parameters, and more. https://www.youtube.com/watch?v=9MHYHgh4jYc

- flash (the flask object): After importing the flash object, you can flash messages on the screen for the user too see. The categories are not necessary but chages the css associated with the messages. https://www.youtube.com/watch?v=qbnqNWXf_tU

- SQLAlchemy: This is a ORM (Object-Relational Mapping) tool for Python. SQLAlchemy simplifies interactions with databases by allowing you to work with Python objects rather than SQL statements directly. https://www.youtube.com/watch?v=AKQ3XEDI9Mw

- Virtual environments: Isolated environment for a python project. This allows you to avoid conflicts between different versions of libraries used by different projects. https://www.youtube.com/watch?v=Y21OR1OPC9A&t=47s

- UserMixin: This is a class provided by the flask_login extension for Flask. IT includes the required methods that Flask-Login needs for managing user sessions. By inheriting from UserMixin, a user model automatically implements these methods.

## Environment Notes

- In a virtual environment with Python 3.12.1

| Package           | Version |
|-------------------|---------|
| blinker           | 1.8.2   |
| click             | 8.1.7   |
| Flask             | 3.0.3   |
| Flask-Login       | 0.6.3   |
| Flask-SQLAlchemy  | 3.1.1   |
| greenlet          | 3.0.3   |
| itsdangerous      | 2.2.0   |
| Jinja2            | 3.1.4   |
| MarkupSafe        | 2.1.5   |
| pip               | 24.1.2  |
| SQLAlchemy        | 2.0.31  |
| typing_extensions | 4.12.2  |
| watchdog          | 4.0.1   |
| Werkzeug          | 3.0.3   |
