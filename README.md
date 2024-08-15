# Active_Recall_Pro (This is a stand-in name)
 A flashcard web app project.
## OVERVIEW:
Active Recall Pro (ARP) is a flash card web application that allows users to create a user account, log in, create multimedia flash cards, edit flash cards, delete flash cards, and study flash cards. Future features will include:

* A social media feature that will allow users to make decks public (so that they may be seen and studied by other users) or private (so that only the creator can see the deck and its cards). 
* A version control feature similar to Git for flashcard decks. This would allow users to copy a public deck to their profile and modify it, or to collaborate on decks using a Git-like branch structure. 
* Stat tracking on who creates popular decks (meaning decks that are studied, copied, and branched often) will allow a ranking or reward system to benefit power-users. 
* Features such as a heat map for studying similar to anki or GitHub, and time view (a view of a deck arranged for studying based on the week of a class one is in) are also possible. 
* An integrate AI using an LLM to read all of the cards in a user's FC database and process the results of their studying. The AI will then make suggesstions for what new cards to make, can change the order of what cards to study next, and articulate the user's strengths and weaknesses to display to the user. 
* Most importantly, users will evevntually own their cards and they will be saved to the user’s machine to be synced to the site later.

This is also a learning project for me to get used to a GIT workflow and creating documentation like this.

Note that this code was HEAVILY commented as I am using it as a learning tool and hope to colaborate on later features, but I am moving that information over to the wiki to clean up the code.

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
    - [x] Put opening paragraph in to list format
    - [x] Add contributor instructions (Git use with video links and written expalnation)
7. Create a wiki pages (https://www.youtube.com/watch?v=bnMl0d-RcPQ)
    - Create wiki page for each page or feature of site or file
    - [x] Move tutorials, links, and notes to wiki.
8. Add landing page
    - Create branch
    - Add landing route in views.py (this is one page)
    - Add landing.html file
9. Enable flashcards to be organized in to decks 
    - Create branch
    - Adjust models.py for new deck model 
    - Add one to many relationship from user to deck and deck to fc
    - Adjust list page to list decks instead of cards
    - Create a "non-deck" for cards that are in no deck but still exist in database
10. Update home now that it does not have card list (will still have card create)
    - Display greeting to user
    - Display list of decks
11. Add edit card feature
    - make branch
    - Allow all cards in the card list to be edited both front and back
12. Enable Images in flashcards
    - Create branch
13. Enable text editor features in card creation. Must persist in future studying.
    - Add spell check?
    - Add bold, italics, underline buttons
    - Add list features
14. Create and admin area: All users, decks, stats are visible
15. Enable spaced repetition algorithm (SM_2?)https://www.youtube.com/watch?v=dF5rY3xQeAQ&t=237s
16. Improve Bootstrap UI
    - Make Nav bar visible
    - Pick a color scheme
    - Create and add a logo?
    - Set fixed minimum size for study page card
    - Add hover text for various buttons (delete card)
    - Create new delete button that looks less terrible
    - Add space bar button press for "show back" and "next card" buttons on study.html
    - Make button placement on flash messages uniform
    - Change log in flash message to a greeting with the user's name
16. Add light mode (assuming dark mode is the default)
    - add dark mode toggle?
18. Add heat Map feature
19. Add Google authentication as an option? (https://www.youtube.com/watch?v=n4e3Cy2Tq3Q)
    - Creating a user account without Google must still be an option
20. Add collaborative/public decks
    - Create branch
    - Add private/public toggle for each deck (default to public)
21. Add Deck copy feature: Cards will be visible before copy and download.
22. Add AI/LLM integration
    - Create branch
    - Select LLM or ChatGPT API
23. Host on AWS (or some similar could service)
24. Add deck branch feature
25. Add school specific feature. Decks can be made for certain classes at specific schools with both topic view and time view for the decks.
26. Monetize with Google ads (AdSense)?
27. Create desktop app (99designs??)
28. Create mobile app (99designs??)

## CONTRIBUTOR INSTRUCTIONS
### I like using GitHub deskptop so these instructions reflect that. You do not have to.
- This is a good overview of GitHub desktop I suggest watching first: https://www.youtube.com/watch?v=8Dd7KRpKeaE
- An short GitHub tutorial (Skip to 1:35) https://www.youtube.com/watch?v=CML6vfKjQss
- A more detailed tutorial https://www.youtube.com/watch?v=HbSjyU2vf6Y

1. Be sure to have a GitHub profile.
2. Download and install GitHub desktop.
3. Go to the ARP project page and click the "fork" button.
4. Pick yourself as the owner and click "create fork". You should now have your own copy of the project on GitHub. 
5. Open GitHub desktop. Be sure to be signed in.
6. Click the clone button on your version of the project on GitHub and copy the URL.
7. In Github desktop, click "file -> clone repository", paste in the project URL, and select the location to which you will save the repository. The files for the project should now be on your machine and in a local repository. https://docs.github.com/en/desktop/adding-and-cloning-repositories/cloning-a-repository-from-github-to-github-desktop
8. Create a branch on your repository. 
9. To open a dev server version of the project, open "main.py" and run it. It should produce a clickable localhost link in the output. Click on this to open ARP in a browser window.
10. Make your code changes.
11. Add, push, and merge your code. This will all be on your copy of the project.
12. When finished, submit a pull request on GitHub.
13. Respond to feedback on the pull request.

## CONTRIBUTOR GUIDELINES
- The most important guideline: If you have a question about how something works, CHECK THE WIKI FIRST.
- Be sure to update the README TODO section by adding an x next to anything  you complete.
- Initial the things from the TODO list that you have completed so yor get credit.
- Add any function you create to the wiki for the related page. 

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
