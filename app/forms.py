from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TimeField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    new_user = SubmitField("New User")
    
class ResponderEntry(FlaskForm):
    entry = SubmitField()

class OperatorForm(FlaskForm):
    location = StringField('Location', validators=[DataRequired()])
    time = TimeField('Time')
    animal = BooleanField('Animal')
    fire = BooleanField('Fire')
    flood = BooleanField('Flood')
    medical = BooleanField('Medical')
    electrical = BooleanField('Electrical')
    other = StringField('Other')
    description = StringField('Description', validators=[DataRequired()])
    update = SubmitField('Update')
    new_event = SubmitField('New Event')
