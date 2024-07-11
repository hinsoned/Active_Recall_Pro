# main.py

# 'website' is a python package thanks to  __init__.py so we can import anything 
# defined in that file.
from website import create_app

app = create_app()

# This if statement checks if the script is being run directly (
# i.e., not being imported as a module in another script). 
# This is determined by checking if __name__ is equal to '__main__'.
if __name__ == '__main__':
    #Change this to false when website is live!!!
    app.run(debug=True, use_reloader=False) # The app.run(debug=True) line starts the Flask development server.
                        # This will also re run the server when code changes are made.