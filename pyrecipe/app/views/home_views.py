"""
Routes for the Flask App.

* index -- main page

TODO:
just have
"/"
"/index"
"/about"
"""

from collections.abc import MutableSequence
from typing import List

import flask
from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
from flask import request
from werkzeug.urls import url_parse


from pyrecipe.frontend import TEMPLATESDIR
from pyrecipe.static import STATICDIR
from pyrecipe.storage import User, Recipe
from pyrecipe.app.helpers.view_modifiers import response
from pyrecipe.app.forms import LoginForm
from pyrecipe.app.forms import RegistrationForm


blueprint = flask.Blueprint('home', __name__, template_folder=str(TEMPLATESDIR), static_folder=str(STATICDIR))


@blueprint.route("/")
@blueprint.route("/index")
@response(template_file="index.html")
def index():
    """
    Routing required for the main page or index.html page.
    Login is required.
    """
    recipes = [r for r in Recipe.objects() if r.deleted==False]
    tags = Recipe.get_tags()
    return {
        "title": "Home Page",
        "recipes": recipes,
        "tags": tags,
        "username": "Tester"
    }
    #return render_template("index.html", title="Home Page", recipes=recipes, tags=tags, username='Tester')


@blueprint.route("/about")
@response(template_file="about.html")
def about():
    return {
        "message": "About Page"
    }

#
#
#@blueprint.route("/login", methods=["GET", "POST"])
#def login():
#    """
#    Routing required for user log-ins.
#    If form is empty: show the empty form.
#    If form is complete: submits form data and flashes a message
#        at the top banner.
#    errors: red banner below required form fields.
#    """
#    if current_user.is_authenticated:
#        return redirect(url_for("index"))
#    form = LoginForm()
#    if form.validate_on_submit():
#        user = User.objects().filter(username=form.username.data).first()
#        if user is None or not user.check_password(form.password.data):
#            flash("Invalid username or password")
#            return redirect(url_for("login"))
#        login_user(user, remember=form.remember_me.data)
#        next_page = request.args.get("next")
#        if not next_page or url_parse(next_page).netloc != "":
#            next_page = url_for("index")
#        return redirect(next_page)
#    return render_template("login.html", title="Sign In", form=form)
#
#
#@blueprint.route("/logout")
#def logout():
#    """Logout the user and return to the index page."""
#    logout_user()
#    return redirect(url_for("index"))
#
#
#@blueprint.route("/registration", methods=["GET", "POST"])
#def register():
#    """
#    Routing required for user registration.
#    If form is empty: show the empty form.
#    If form is complete: submits form data and flashes a message
#        at the top banner.
#    errors: red banner below required form fields.
#    """
#    if current_user.is_authenticated:
#        return redirect(url_for("index"))
#    form = RegistrationForm()
#    if form.validate_on_submit():
#        user = User(name=form.name.data, username=form.username.data.lower(), email=form.email.data.lower())
#        user.set_password(form.password.data)
#        user.save()
#        flash("Congratulations, you are now a registered user!")
#        return redirect(url_for("login"))
#    return render_template("register.html", title="Register", form=form)
#
#
#@blueprint.route("/user/<username>")
#def user(username:str):
#    """
#    Routing required for user profile pages.
#
#    :param username: (str) the username of the user.
#
#    :returns: user profile informatin or 404 if user is not found.
#    """
#    user = User.objects().filter(username=username).first()
#    if not user:
#        flask.abort(404)
#    recipes = [recipe for recipe in user.recipe_ids if recipe.deleted==False]
#    return render_template('user.html', user=user, recipes=recipes)


#@blueprint.route("/user/<username>/deleted")
#def deleted(username:str):
#    """
#    Routing required for user profile pages.
#
#    :param username: (str) the username of the user.
#
#    :returns: user profile informatin or 404 if user is not found.
#    """
#    user = User.objects().filter(username=username).first()
#    if not user:
#        flask.abort(404)
#    recipes = [recipe for recipe in user.recipe_ids if recipe.deleted==True]
#    return render_template('user.html', user=user, recipes=recipes)
#
#
#@blueprint.route("/recipe/view/<recipe_id>")
#def recipe_view(recipe_id:str):
#    """
#    Routing required to view a recipe's details.
#
#    :param recipe_id: (str) the DB id of the recipe.
#
#    :returns: recipe or 404 if recipe is not found.
#    """
#    recipe = Recipe.objects().filter(id=recipe_id).first()
#    if not recipe:
#        flask.abort(404)
#    return render_template("recipe.html", recipe=recipe)
#
#@blueprint.route("/recipe/add", methods=["GET", "POST"])
#def recipe_add():
#    pass
#
#
#@blueprint.route("/recipe/edit/<recipe_id>", methods=["GET", "POST"])
#def recipe_edit():
#    pass
#
#
#@blueprint.route("/tag/<tags>")
#def tag(tags: List[str]):
#    """
#    Routing required to view recipes with a given tag.
#
#    :param recipe_id: (str) the DB id of the recipe.
#
#    :returns: recipe or 404 if recipe is not found.
#    """
#    if not isinstance(tags, MutableSequence):
#        tags = [tags]
#    recipes = Recipe.find_recipes_by_tag(tags)
#    return render_template("tag.html", recipes=recipes)


