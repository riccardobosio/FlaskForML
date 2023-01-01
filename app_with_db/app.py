from flask import Flask, flash, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

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

from forms import RegistrationForm, LoginForm

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created, you can now login')
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        pass
    return render_template('login.html', title='Login', form=form)

@app.route("/predictions", methods=['GET'])
def get_predictions():
    pass

@app.route("/predict", methods=['GET', 'POST'])
def make_prediction():
    pass

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')