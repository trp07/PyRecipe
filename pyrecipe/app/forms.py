"""Classes to store web-form data."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from pyrecipe.storage import User


class LoginForm(FlaskForm):
    """A class to store data for a login form."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    """A class to store user registration data."""
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        """Ensure repeat usernames aren't registered."""
        user = User.objects().filter(username=username.data.lower()).first()
        if user:
            raise ValidationError("Username in use.  Please use a different username.")

    def validate_email(self, email):
        """Ensure repeat email addresses aren't registered."""
        user = User.objects().filter(email=email.data.lower()).first()
        if user:
            raise ValidationError("Email address in use.  Please use a different email address.")
