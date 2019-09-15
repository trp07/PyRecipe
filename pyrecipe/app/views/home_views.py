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
from pyrecipe.app.helpers.view_modifiers import response
from pyrecipe.app.viewmodels.home import IndexViewModel
from pyrecipe.app.viewmodels.home import AboutViewModel


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
    vm.get_recipes()

    return vm.to_dict()


@blueprint.route("/about")
@response(template_file="home/about.html")
def about():
    vm = AboutViewModel()
    return vm.to_dict()
