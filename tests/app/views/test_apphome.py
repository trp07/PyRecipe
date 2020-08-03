"""Tests for pyrecipe/app/views."""

import pytest

from flask import Response

from pyrecipe.usecases.account_uc import AccountUC
from pyrecipe.usecases.recipe_uc import RecipeUC
from pyrecipe.app import app as flask_app
from pyrecipe.app.views import home_views
from pyrecipe.app.viewmodels.home import IndexViewModel
from pyrecipe.app.viewmodels.home import AboutViewModel


def test_indexview(mocker):
    """
    GIVEN a running app
    WHEN a view is requested for /index
    THEN assert no errors
    """
    acct = mocker.patch.object(AccountUC, "find_user_by_id")
    recipes = mocker.patch.object(RecipeUC, "get_all_recipes")
    tags = mocker.patch.object(RecipeUC, "get_tags")
    idxvm = mocker.patch.object(IndexViewModel, "__call__")

    with flask_app.test_request_context(path="/index", data=None):
        resp: Response = home_views.index()
    assert resp.location is None


def test_aboutview(mocker):
    """
    GIVEN a running app
    WHEN a view is requested for /about
    THEN assert no errors
    """
    acct = mocker.patch.object(AccountUC, "find_user_by_id")
    aboutvm = mocker.patch.object(AboutViewModel, "__call__")

    with flask_app.test_request_context(path="/about", data=None):
        resp: Response = home_views.about()
    assert resp.location is None

