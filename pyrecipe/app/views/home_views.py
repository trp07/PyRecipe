"""
Routes for the Flask App.

* index -- main page
* about -- information about the project
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
