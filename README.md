# Active_Recall_Pro (This is a stand-in name)
 A flashcard web app project.
## GOAL:
The immediate goal is to create a flash card web application that allows users to log in, create multimedia flash cards, edit flash cards, delete flash cards, and study flash cards. The long term plan is to add a social feature that would allow users to make decks public (so that they may be seen and studied by other users) or private (so that only the creator can see the deck and its cards). I also hope to add a version control feature similar to Git for flashcard decks. This would allow users to copy a public deck to their profile and modify it, or to collaborate on decks using a Git-like branch structure. Tracking stats on who creates popular decks (meaning decks that are studied, copied, and branched often) could allow a ranking or reward system to benefit power-users. Features such as a heat map for studying similar to anki or GitHub, and time view (a view of a deck arranged for studying based on the week of a class one is in) are also possible. Most importantly, users wiil evevntually own their cards and they will be saved to the user’s machine to be synced to the site later.

This is also a learning project for me to get used to a GIT workflow and creating documentation like this.

Note that this code will be HEAVILY commented as I am using it as a learning tool and hope to colaborate on later features.

## TODO / KNOWN ISSUES:
1. Create initial notes app following tutorial: https://www.youtube.com/watch?v=dam0GPOAvVI
    - [x] Figure out pyache issue. What is it?
    - [x] Understand secret key from __init__.py
    - [x] Understand @ symbol in relation to routes.
2. Find a way to see what is in database at any time.
    - [x] DB Browser for SQL lite https://sqlitebrowser.org/dl/
3. Convert Notes to flashcards
    - [x] Create branch
    - [x] change model in model.py
    - [x] change note creation in home.html
    - [x] change / route in views.py
    - [x] fix __init__.py import
    - [x] update base.html delete card function
    - [x] update views.html deltecard fuction
    - [x] label front and back of cards in form
4. Create study mode
    - [x] Add study mode route to views.py
    - [x] Display one card front with "flip" button to study
    - [x] Next Card button appears only after card is flipped 
    - [x] Add study mode button to home and to nav bar
5. Add general dark theme
    - [x] update bootstrap version to 5.3.3
    - [x] add dark mode code to html tag on base.html: data-bs-theme="dark" 
    - [x] update font awesome link
    - [x] fix model close button issue
    - [x] fix model close button position
    - [x] fix card delete button position
    - [x] Make study page buttons full width (not related I just wanted to)
6. Learn about README file standards and update this file.
7. Add Flashcards list page. Just display both sides of all cards sequentially.
    - Add card list and card create route in views.py (this is one page)
    - Add card create on this page as well
    - This will eventually hold a list of decks instead of cards (see step 10)
8. Update home now that it does not have card list (will still have card create)
    - Display greeting to user
    - Display total number of cards
    - Display most recently added card?
    - Graph of cards studied in last month?
9. Enable Images in flashcards
10. Enable flashcards to be organized in to decks 
    - Adjust list page to list decks instead of cards
11. Create and admin area: All users, decks, stats are visible
12. Enable spaced repetition algorithm (SM_2?)https://www.youtube.com/watch?v=dF5rY3xQeAQ&t=237s
13. Improve Bootstrap UI
    - Make Nav bar visible
    - Pick a color scheme
    - Create and add a logo?
    - Set fixed minimum size for study page card
14. Add light mode (assuming dark mode is the default)
    - add dark mode toggle?
15. Add heat Map feature
16. Add Google authentication as an option? (https://www.youtube.com/watch?v=n4e3Cy2Tq3Q)
    - Creating a user account without Google must still be an option
17. Add collaborative/public decks
18. Add Deck copy feature: Cards will be visible before copy and download.
19. Host on AWS (or some similar could service)
20. Add deck branch feature
21. Add school specific feature. Decks can be made for certain classes at specific schools with both topic view and time view for the decks.
22. Create desktop app (99designs??)
23. Create mobile app (99designs??)

## RELEVANT TUTORIALS:
1. To follow for creation of a notes App. Includes information on file structure, use of Flask,  and SQL integration https://www.youtube.com/watch?v=dam0GPOAvVI
2. For installation of python, PIP, and general Flask,https://www.youtube.com/watch?v=Z1RJmh_OqeA
3. Blueprints in flask https://www.youtube.com/watch?v=WteIH6J9v64
4. Bootstrap tutorial long: https://www.youtube.com/watch?v=-qfEOE4vtxE
5. Bootstrap tutorial short: https://www.youtube.com/watch?v=eow125xV5-c
6. Admin area https://www.youtube.com/watch?v=WqHtmz8Ibn8
7. Tkinter https://www.youtube.com/watch?v=Pd3XoLSQ5wg
8. Make a good README https://www.youtube.com/watch?v=a8CwpGARAsQ https://www.youtube.com/watch?v=E6NO0rgFub4

## RELEVANT LINKS:
1. Bootstrap. open source CSS Framework used in the main tutorial:https://www.youtube.com/watch?v=eow125xV5-c Home page: https://getbootstrap.com/
2. Flask-Admin https://flask-admin.readthedocs.io/en/latest/
3. Flask Documentation: https://flask.palletsprojects.com/en/3.0.x/

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

- GitHub Desktop: https://www.youtube.com/watch?v=8Dd7KRpKeaE

- __name__ :This is a special built-in variable that represents the name of the current module. When a module is run directly, __name__ is set to '__main__'. When the module is imported, __name__ is set to the module's name. By passing __name__ to Flask, you tell Flask that the root path of the application is the directory containing app.py. This way, Flask knows to look for templates in the templates directory and static files in the static directory.

- login_user(user, remember=True) : The remember parameter, when set to True, uses a secure cookie to remember the user after the session ends. This allows the user to stay logged in even after closing the browser.

- python decorators: Decorators ( or the @ symbol fllowed by text) can be used on functions, classes, or methods. It is a function that accepts a function and returns a function. Functions in python can be nested in python, think of a decorator as a function in to which the function, classe, or method it is above is passed in to. https://www.youtube.com/watch?v=WpF6azYAxYg https://www.youtube.com/watch?v=BE-L7xu8pO4

- LoginManager: The LoginManager keeps track of the logged-in user during a session. It provides a way to "remember" the user between requests and handle login/logout functionality. login_manager.init_app(app) links the LoginManager instance to the Flask app, enabling its functionality within the application. This will automatically add a "Please log in to access this page" flash message.

- Secret Key (as seen in __init__py): (From the flask website) A secret key that will be used for securely signing the session cookie and can be used for any other security related needs by extensions or your application. It should be a long random bytes or str.

- __pyache__ : When you run a Python script, the Python interpreter compiles it into bytecode. This bytecode is a lower-level, platform-independent representation of your source code. If Python had to compile your scripts every time you ran them, it would slow things down. Instead, it stores the compiled bytecode in the __pycache__ directory. The next time you run your script, Python can skip the compilation step if the bytecode is already up-to-date

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
