# __init__.py
from flask import Flask

# This is a factory function that creates a flask instance.
# '__name__' is a special variable that indicates the current module ( .py file)
def create_app():
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'Brooklyn Nets'

        from .views import views
        from .auth import auth

        #These make the path to access the routes in the blueprints available.
        #The url prefix for both views in both will be '/'
        app.register_blueprint(views, url_prefix='/')
        app.register_blueprint(auth, url_prefix='/')

        return app