from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, user_loaded_from_request
from flask.sessions import SecureCookieSessionInterface
import os


#@user_loaded_from_request.connect
def user_loaded_from_request(app, user=None):
    g.login_via_request = True

class CustomSessionInterface(SecureCookieSessionInterface):
    """Prevent creating session from API requests."""
    def should_set_cookie(self, *args, **kwargs):
        return False

    def save_session(self, *args, **kwargs):
        if g.get('login_via_request'):
            return
        return super(CustomSessionInterface, self).save_session(*args, **kwargs)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('HOODCAST_SECRET_KEY', None)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hoodcast.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.session_interface = CustomSessionInterface()

db = SQLAlchemy(app)
port = int(os.environ.get("PORT", 5000))

login = LoginManager()
login.login_view = 'login'
login.init_app(app)
    
import routes, models

if __name__ == '__main__':
    app.run(debug=True)
