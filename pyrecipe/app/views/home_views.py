"""
Routes for the Flask App.

* index -- main page
* about -- information about the project
"""

from collections.abc import MutableSequence
from typing import List

import flask
from flask import current_app

from pyrecipe.app.helpers.view_modifiers import response
from pyrecipe.app.viewmodels.home import IndexViewModel
from pyrecipe.app.viewmodels.home import AboutViewModel
from pyrecipe.frontend import TEMPLATESDIR
from pyrecipe.static import STATICDIR
from pyrecipe.usecases.recipe_uc import RecipeUC


blueprint = flask.Blueprint(
    "home", __name__, template_folder=str(TEMPLATESDIR), static_folder=str(STATICDIR)
)


@blueprint.route("/")
@blueprint.route("/index")
@response(template_file="home/index.html")
def index():
    """
    Routing required for the main page or index.html page.
    Login not required.
    """
    vm = IndexViewModel()
    vm.validate()

    uc = RecipeUC(current_app.config["DB_DRIVER"])
    vm.recipes = uc.get_all_recipes(deleted=False)
    vm.tags = uc.get_tags()

    return vm.to_dict()


@blueprint.route("/about")
@response(template_file="home/about.html")
def about():
    vm = AboutViewModel()
    flask.flash("This page is not yet developed", category="warning")
    return vm.to_dict()
