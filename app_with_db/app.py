from flask import Flask 
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(50))

    def __repr__(self):
        return f"User({self.id}, {self.email})"

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    home = db.Column(db.String(20))
    away = db.Column(db.String(20))

    def __repr__(self):
        return f"Event({self.id}, {self.home}, {self.away})"

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    result = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

@app.route("/predictions", methods=["GET"])
def get_predictions():
    pass

@app.route("/predict", methods=["GET", "POST"])
def make_prediction():
    pass