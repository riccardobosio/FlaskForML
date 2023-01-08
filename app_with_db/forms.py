from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from app import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email: # check only if the update is different from current name
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class PredictionForm(FlaskForm):
    event_id = IntegerField('Event', validators=[DataRequired()])
    result = IntegerField('Result', validators=[DataRequired()])#Length(min=1, max=1, message='Prediction should be 0 (draw), 1 (home wins), 2 (away wins)')
    submit = SubmitField('Predict')

class EventForm(FlaskForm):
    home = StringField('Home', validators=[DataRequired()])
    away = StringField('Away', validators=[DataRequired()])
    submit = SubmitField('Create event')