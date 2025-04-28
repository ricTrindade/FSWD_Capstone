from dotenv import load_dotenv
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Load environment variables from .env file
load_dotenv()

# Access variables
database_url = os.getenv("DATABASE_URL")
flask_app = os.getenv("FLASK_APP")
flask_env = os.getenv("FLASK_ENV")

# App & DB Config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_APP'] = flask_app
app.config['FLASK_ENV'] = flask_env
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Movie Model
class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    release_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<Movie {self.title}>"

# Actor Model
class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"<Actor {self.name}>"





