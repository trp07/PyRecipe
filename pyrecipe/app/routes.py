"""
Routes for the Flask App.

* index -- main page
* login -- user logins
* logout -- user logouts
* register -- user registration
* user -- user profile page
* recipe -- view a specific recipe
"""

import flask
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from pyrecipe.app import app
from pyrecipe.app.forms import LoginForm, RegistrationForm
from pyrecipe.storage import User, Recipe


@app.route("/")
@app.route("/index")
@login_required
def index(method=["GET"]):
    """
    Routing required for the main page or index.html page.
    Login is required.
    """
    recipes = list(Recipe.objects().filter())
    return render_template("index.html", title="Home Page", recipes=recipes)


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Routing required for user log-ins.
    If form is empty: show the empty form.
    If form is complete: submits form data and flashes a message
        at the top banner.
    errors: red banner below required form fields.
    """
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects().filter(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    """Logout the user and return to the index page."""
    logout_user()
    return redirect(url_for("index"))


@app.route("/registration", methods=["GET", "POST"])
def register():
    """
    Routing required for user registration.
    If form is empty: show the empty form.
    If form is complete: submits form data and flashes a message
        at the top banner.
    errors: red banner below required form fields.
    """
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, username=form.username.data.lower(), email=form.email.data.lower())
        user.set_password(form.password.data)
        user.save()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/user/<username>")
@login_required
def user(username:str):
    """
    Routing required for user profile pages.

    :param username: (str) the username of the user.

    :returns: user profile informatin or 404 if user is not found.
    """
    user = User.objects().filter(username=username).first()
    if not user:
        flask.abort(404)
    recipes = [recipe for recipe in user.recipe_ids]
    return render_template('user.html', user=user, recipes=recipes)


@app.route("/user/recipe/<recipe_id>")
@login_required
def recipe(recipe_id:str):
    """
    Routing required to view a recipe's details.

    :param recipe_id: (str) the DB id of the recipe.

    :returns: recipe or 404 if recipe is not found.
    """
    recipe = Recipe.objects().filter(id=recipe_id).first()
    if not recipe:
        flask.abort(404)
    return render_template('recipe.html', recipe=recipe)
