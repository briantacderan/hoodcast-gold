from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('MAILGUN_SECRET_KEY', None)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hoodcast.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

port = int(os.environ.get("PORT", 5000))

import routes, models

if __name__ == '__main__':
    app.run(debug=True)
