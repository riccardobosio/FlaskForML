from flask import Flask, flash, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from flask_migrate import Migrate
import secrets
import os
from PIL import Image


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info' # for bootstrap

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(50))
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    def __repr__(self):
        return f"User({self.id}, {self.email})"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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

# IMPORT FORMS
from forms import RegistrationForm, LoginForm, UpdateAccountForm, PredictionForm, EventForm

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash("You are already logged in.")
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created with email {form.email.data}, you can now login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.")
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check your email and pw', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/')
@app.route('/home')
def home():
    predictions = Prediction.query.all()
    return render_template('home.html', predictions=predictions)

@app.route('/logout')
def logout():
    logout_user()
    flash("You logged out.")
    return redirect(url_for('home'))

def save_picture(form_picture):
    # randomize name of the file
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been update', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route('/event/new', methods = ['GET', 'POST'])
@login_required
def new_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(home=form.home.data, away=form.away.data)
        db.session.add(event)
        db.session.commit()
        flash('The event has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_event.html', title='New event', form=form)

@app.route('/prediction/new', methods=['GET', 'POST'])
@login_required
def new_prediction():
    form = PredictionForm()
    if form.validate_on_submit():
        prediction = Prediction(result=form.result.data, event_id=form.event_id.data, user_id=current_user.id)
        db.session.add(prediction)
        db.session.commit()
        flash('Your prediction has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_prediction.html', title='New prediction', form=form)

@app.route('/event', methods=['GET'])
@login_required
def get_event():
    events = Event.query.all()
    return render_template('get_event.html', title='Events list', events=events)
