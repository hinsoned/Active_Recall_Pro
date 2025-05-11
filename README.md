# Active_Recall_Pro (This is a stand-in name)

A flashcard web app project.

## OVERVIEW:

Active Recall Pro (ARP) is a flash card web application that allows users to create a user account, log in, create multimedia flash cards, edit flash cards, delete flash cards, and study flash cards. Future features will include:

- A social media feature that will allow users to make decks public (so that they may be seen and studied by other users) or private (so that only the creator can see the deck and its cards).
- A version control feature similar to Git for flashcard decks. This would allow users to copy a public deck to their profile and modify it, or to collaborate on decks using a Git-like branch structure.
- Stat tracking on who creates popular decks (meaning decks that are studied, copied, and branched often) will allow a ranking or reward system to benefit power-users.
- Features such as a heat map for studying similar to anki or GitHub, and time view (a view of a deck arranged for studying based on the week of a class one is in) are also possible.
- An integrate AI using an LLM to read all of the cards in a user's FC database and process the results of their studying. The AI will then make suggesstions for what new cards to make, can change the order of what cards to study next, and articulate the user's strengths and weaknesses to display to the user.
- Most importantly, users will evevntually own their cards and they will be saved to the user’s machine to be synced to the site later.

This is also a learning project for me to get used to a GIT workflow and creating documentation like this.

Note that this code was HEAVILY commented as I am using it as a learning tool and hope to colaborate on later features, but I am moving that information over to the wiki to clean up the code.

## TODO / KNOWN ISSUES:

1. Create initial notes app following tutorial: https://www.youtube.com/watch?v=dam0GPOAvVI
   - [x] Figure out pyache issue. What is it?
   - [x] Understand secret key from **init**.py
   - [x] Understand @ symbol in relation to routes.
2. Find a way to see what is in database at any time.
   - [x] DB Browser for SQL lite https://sqlitebrowser.org/dl/
3. Convert Notes to flashcards
   - [x] Create branch
   - [x] change model in model.py
   - [x] change note creation in home.html
   - [x] change / route in views.py
   - [x] fix **init**.py import
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
   - [x] Create branch
   - [x] Add landing route in views.py as alternate to home page
   - [x] Add landing.html file
9. Enable flashcards to be organized in to decks
   - [x] Create branch
   - [x] Adjust models.py for new deck model
   - [x] Add one to many relationship from user to deck and deck to fc
   - [x] Add 'create deck' button to home page
   - [x] Adjust home page to list decks instead of cards
     - [x] Update home route to pass in list of all decks
     - [x] change home.html to display bootstrap cards for each deck
     - [x] create a route for viewing each deck.
   - [x] Add clickable card for each deck to navigate to a deck page with a card list
   - [x] Make study button on each deck page fuctional
   - [x] Add study button to each deck on Home page
   - [x] Remove top study button
   - [x] Add create card form and study button to deck pages.
   - [x] Add card delete button to each card on view deck page (fetch?)
   - [x] Add deck delete button to each Deck on Decks page
10. Contributor Instructions update
    - Add information about virtual environments
    - Update environment notes if needed
    - Add option for using DB Browser
11. Fix refresh issue for cards and decks
    - [x] Create branch
    - [x] Cause new cards to load immediately when created on deck page. (AJAX or fetch?)
      - [x] Flash messages may be impossible now, create some equivalent: works for failure to make card
      - [x] Add flash message for creating a new card
    - [x] Cause new decks to load immediately when created on deck page. (AJAX or fetch?)
      - [x] Flash messages may be impossible now, create some equivalent: works for failure to make deck
      - [x] Add flash messages for creating new decks
12. Create new .py file for fetch related end points
    - [x] import and register in **init**.py
    - [x] move code for these end points
    - [x] update necessary imports
13. Update home now that it does not have card list (will still have card create)
    - [x] Display list of decks
    - [x] Add number of cards in each deck to each deck on home page
14. Add edit card feature
    - [x] Make branch
    - [x] Allow all cards in the card list to be edited both front and back
      - [x] Add edit button to each card in card list
      - [x] Add "edit-card" end point to views.py
      - [x] Create edit_card html file
15. Change study page to allow dynamic card retrieval from database
    - [x] Create branch
    - [x] Remove hidden div html from study.html
    - [x] Update javascript in study.html to use fetch
    - [x] Add necessary GET endpoints to actions.py
16. Enable Images in flashcards
    - Create branch
17. Enable text editor features in card creation. Must persist in future studying.
    - [x] Create Brach
    - [x] Quilljs
      - [x] Add bold, italics, underline buttons
      - [x] Add list features
      - [x] Use safe to allow for render of HTML created by quiljs RTE (jinja security concerns?)
    - [x] Prevent addition of blank card
    - [x] Prevent the addition of only cards with only spaces on them
18. Enable rich text editor for card edit.
    - [x] Create Branch
    - [x] Fix existing text display in card edit window (currently appearing as HTML): Replace textarea with div for Quill editors.
    - [x] Add RTE to Card edit display. Initialize Quill editors in script section.
19. Move JS to separate files
    - [x] Create Branch
    - [x] Move all JS to new files (leave heat map for now)
20. Update Storage from RTE (fix card edit with RTE issue)
    - [x] Create Branch
    - [x] Move to Delta Format for storage of Quill
    - [x] Move card display on view_deck to javascript from jinja
    - [x] Update edit card
21. Log in card visibility
    - [x] Update card visibility such that it decks only appear for their associated user
22. Card list appearance update on Decks view
    - [x] Create branch 
    - [x] Change HTML to take full width of screen
    - [x] Set max height? (optional)
23. Separate Home and Profile pages
    - [x] Create branch
    - [x] Create new Flask endpoint
    - [x] Create new HTML and JS files for this Home page
    - [x] Rename all Profile page elements
24. Enable spaced repetition algorithm (SM_2?)https://www.youtube.com/watch?v=dF5rY3xQeAQ&t=237s
    - [x] Create branch
    - [x] Update models with new fields
    - [x] Create two deck modes for studying.
25. Add QOL links to Study and Decks page.
    - [x] Create branch
    - [x] Add link back to deck page from study page
26. Add Deck mode switch
    - [x] Create Branch
    - [x] Update UI
    - [x] Add endpoint in actions to change db information
27. Add username to signup
    - [x] Update sign_up.html
    - [x] Update models.py
    - [x] Update Auth endpoint
28. Add ability to view other user's profiles
    - [x] create branch
    - [x] Create profile template for other users (view_profile)
    - [x] update route
    - [x] Generate deck List (no study or delete or view options yet)
    - [x] Make username visible on Home and on all profiles
    - [x] Make email visible on profile
    - [x] Remove names from view_profile.html
    - [x] Add username to model
    - [x] ensure that attempting to view your own view_profile page reroutes users to profile
29. Add ability to view other peoples decks
    - [x] create branch
    - [x] Add a user list with links to profile on home.html
    - [x] Add deck list to view_profile page
    - [x] Add "view deck" button to view_profile page
    - [x] Add links from deck view to deck owner profile
    - [x] Add card count to view_public_deck pages
30. Add card movement between decks
    - [x] Create branch
    - [x] Add deck options drop down to view_deck page
    - [x] Update view_deck.js to handle dropdown
    - [x] Create new moveCard route in actions.py
31. Add modal warning on deck delete
    - [x] Create branch
    - [x] Check for needed imports
    - [x] Add modal
32. Add deck copying
    - [x] Create branch
    - [x] Add copy button to each deck on view_public_deck page
    - [x] Handle new button in view_public_deck.js
    - [x] Add copy deck route to actions.py
    - [x] Add link to profile in success message
33. Add user stats to home page
    - [x] Create Branch
    - [x] Add total cards
    - [x] Add total decks
34. Add user stats to profile page
    - [x] Create branch
    - [x] Add total cards
    - [x] Add total decks
    - [x] Hover added to home page list
35. Deck Heritage System
    - [x] Create branch
    - [x] Update models to add a studycredit model
    - [x] Update FlashCard model
    - [x] Add function to get recent credits to User
    - [x] Add credit information to home page (temporary)
36. DH system refinement / Dev page to see Deck heritage working
    - [x] Create Branch
    - [x] Review and refine DH system
        - [x] Send only one card from back end in SM-2 study
        - [x] Stop users from getting credit via heritage system for studying their own cards
        - [x] Reset original creator and heritage chain fields upon card edit.
37. Add deck list/stats to home page
    - [x] Create Branch
    - [x] Update home.html view for users (make it a list?)
    - [x] Add deck number to user list
    - [x] Add card number to user list
38. Add deck liking (social media aspects)
    - Create Branch
39. Card sanitize
    - Create Branch
    - Update create card (sanitize content on server side, add server-side validation to avoid empty cards)
40. Deck comment sections
    - Create Branch
41. Build dev/admin page
    - Create Branch
    - All users, decks, stats are visible
    - Visualization for deck heritage
42. Enable images on flash cards
    - Create branch
43. Re-enable heatmap
    - Create branch
    - Remake heatmap
    - embed on profile 
    - embed on view_profile pages
    - embed on deck pages
44. Create card search funtionality
    - Create branch
    - Allow users to search through their cards based on the cards text content.
45. Add User avatar to profile creation
    - Create branch
    - Update model
    - Select generic avatar
    - update Profile page
    - update view_profile page
46. Improve Bootstrap UI
    - Cause card creation error to vanish after some time.
    - Display greeting to user
    - Make Nav bar visible
    - Pick a color scheme
    - Create and add a logo?
    - Set fixed minimum size for study page card
    - Add hover text for various buttons (delete card)
    - Create new delete button that looks less terrible
    - Add space bar button press for "show back" and "next card" buttons on study.html
    - Make button placement on flash messages uniform
    - Change log in flash message to a greeting with the user's name
47. Add light mode (assuming dark mode is the default)
    - [x] add dark mode toggle?
48. Add heat Map feature
    - [x] create branch
    - [x] add heat_map.html
49. Add Google authentication as an option? (https://www.youtube.com/watch?v=n4e3Cy2Tq3Q)
    - Creating a user account without Google must still be an option
50. Add collaborative/public decks
    - Create branch
    - Add private/public toggle for each deck (default to public)
51. Add Deck copy feature: Cards will be visible before copy and download.
52. Add AI/LLM integration
    - Create branch
    - Select LLM or ChatGPT API
53. Host on AWS (or some similar could service)
54. Add deck branch feature
55. Add school specific feature. Decks can be made for certain classes at specific schools with both topic view and time view for the decks.
56. Monetize with Google ads (AdSense)?
57. Create desktop app (99designs??)
58. Create mobile app (99designs??)

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
- Be sure to update the README TODO section by adding an x next to anything you complete.
- When you add a function, include a single line comment that explains it in plain English.
- Initial the things from the TODO list that you have completed so yor get credit.
- Add any function you create to the wiki for the related page so that other conrtibutors can understand it.

## Environment Notes

- In a virtual environment with Python 3.12.1

| Package           | Version |
| ----------------- | ------- |
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
