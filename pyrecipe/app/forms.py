"""Classes to store web-form data."""

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms import SubmitField
from wtforms import FieldList
from wtforms import FloatField
from wtforms import IntegerField
from wtforms import FormField
from wtforms.validators import ValidationError
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import EqualTo

from pyrecipe.storage import User


class LoginForm(FlaskForm):
    """A class to store data for a login form."""
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember_me = BooleanField(label='Remember Me')
    submit = SubmitField(label='Sign In')


class RegistrationForm(FlaskForm):
    """A class to store user registration data."""
    name = StringField(label="Name", validators=[DataRequired()])
    username = StringField(label="Username", validators=[DataRequired()])
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    password2 = PasswordField(label="Repeat Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField(label="Register")

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


class IngredientForm(FlaskForm):
    """A class to create and edit recipe ingredients."""
    name = StringField(label="Name", validators=[DataRequired()])
    quantity = StringField(label="Quantity", validators=[DataRequired()])
    unit = StringField(label="Unit of Measurement", validators=[])
    preparation = StringField(label="Preparation of Ingredient", validators=[])


class RecipeForm(FlaskForm):
    """A class to create and edit a recipe."""
    name = StringField(label="Name", validators=[DataRequired()])
    prep_time = FloatField(label="Prep Time (minutes)", validators=[DataRequired()])
    cook_time = FloatField(label="Cook Time (minutes)", validators=[DataRequired()])
    servings = IntegerField(label="Servings", validators=[DataRequired()])
    ingredients = FieldList(unbound_field=FormField(IngredientForm))
    directions = FieldList(unbound_field=StringField(label="Directions", validators=[DataRequired()]))
    tags = StringField(label="Tags", validators=[DataRequired()])
    notes = FieldList(unbound_field=StringField(label="Notes", validators=[DataRequired()]))
    rating = FloatField(label="Rating", validators=[DataRequired()])
    favorite = BooleanField(label="Favorite", validators=[DataRequired()])
