"""Tests for pyrecipe/app/views."""

import pytest

import flask
from flask import Response
import werkzeug

from pyrecipe.usecases.recipe_uc import RecipeUC
from pyrecipe.usecases.account_uc import AccountUC
from pyrecipe.app.viewmodels.recipe import RecipeViewModel
from pyrecipe.app.viewmodels.recipe import AddViewModel
from pyrecipe.app.viewmodels.recipe import EditViewModel
from pyrecipe.app.viewmodels.recipe import DeleteViewModel
from pyrecipe.app import app as flask_app
from pyrecipe.app.views import recipe_views


#################### Recipe Viewing #########################

def test_recipes_all(mocker):
    """
    GIVEN recipes in the DB
    WHEN http request to /recipes/all is initiated
    THEN assert no errors and Not Implemented returned
    """
    rec = mocker.patch.object(RecipeUC, "get_all_recipes")
    rec.return_value = ["recipe1", "recipe2"]
    with flask_app.test_request_context(path="/recipe/all", data=None):
        resp: Response = recipe_views.recipes_all()
    assert resp == "Not Implemented... yet"


def test_recipe_view_found(mocker, testrecipe):
    """
    GIVEN a valid recipe id
    WHEN requesting to view it, /recipe/view/<recipe_id>
    THEN assert no errors in viewing
    """
    rec_data = {
        "name": "test recipe",
        "prep_time": 5,
        "cook_time": 5,
        "servings": 1,
        "ingredients": ["garlic", "onion"],
        "directions": ["cook"],
        "notes": ["this was just a test!"],
        "tags": ["test"]
    }
    find = mocker.patch.object(AccountUC, "find_user_by_id")
    rec = mocker.patch.object(RecipeUC, "find_recipe_by_id")
    rec.return_value = testrecipe(**rec_data)
    vm = mocker.patch.object(RecipeViewModel, "__call__")
    with flask_app.test_request_context(path="/recipe/view/<recipe_id>", data=None):
        resp: Response = recipe_views.recipe_view("1234")
    assert resp.location is None


def test_recipe_view_Notfound(mocker):
    """
    GIVEN an invalid recipe id
    WHEN requesting to view it, /recipe/view/<recipe_id>
    THEN assert 404, NotFound error is thrown
    """
    find = mocker.patch.object(AccountUC, "find_user_by_id")
    rec = mocker.patch.object(RecipeUC, "find_recipe_by_id")
    rec.return_value = None
    vm = mocker.patch.object(RecipeViewModel, "__call__")
    with pytest.raises(werkzeug.exceptions.NotFound):
        with flask_app.test_request_context(path="/recipe/view/<recipe_id>", data=None):
            resp: Response = recipe_views.recipe_view("1234")


#################### Recipe Adding ##########################

def test_recipe_add_get_loggedin(mocker):
    """
    GIVEN a logged-in user
    WHEN navigating to /recipe/add
    THEN assert no errors
    """
    find = mocker.patch.object(AccountUC, "find_user_by_id")
    find.return_value = "FOUND"
    vm = mocker.patch.object(AddViewModel, "__call__")
    with flask_app.test_request_context(path="/recipe/add", data=None):
        resp: Response = recipe_views.recipe_add_get()
    assert resp.location is None


def test_recipe_add_get_loggedout(mocker):
    """
    GIVEN a logged-out or unregistered user
    WHEN navigating to /recipe/add
    THEN assert redirected to login page
    """
    find = mocker.patch.object(AccountUC, "find_user_by_id")
    find.return_value = None
    vm = mocker.patch.object(AddViewModel, "__call__")
    with flask_app.test_request_context(path="/recipe/add", data=None):
        resp: Response = recipe_views.recipe_add_get()
    assert resp.location in ("/account/login", "/login")


def test_recipe_add_post_loggedout(mocker):
    """
    GIVEN a logged-out or unregistered user
    WHEN attempting to post to /recipe/add
    THEN assert redirected to login page
    """
    rec_data = {
        "name": "test recipe",
        "prep_time": "5",
        "cook_time": "5",
        "servings": "1",
        "ingredients": ["garlic", "onion"],
        "directions": ["cook"],
        "notes": ["this is a test"],
        "tags": ["test"],
    }
    find = mocker.patch.object(AccountUC, "find_user_by_id")
    find.return_value = None
    vm = mocker.patch.object(AddViewModel, "__call__")
    rec = mocker.patch.object(RecipeUC, "__call__")
    rec.return_value.create_recipe.return_value = "CREATED"
    with flask_app.test_request_context(path="/recipe/add", data=rec_data):
        resp: Response = recipe_views.recipe_add_post()
    assert resp.location in ("/login", "/account/login")


def test_recipe_add_post_loggedin_created(mocker, testrecipe):
    """
    GIVEN a logged-in user
    WHEN posting to /recipe/add
    THEN no errors and redirected to recipe/view/<recipe_id> page
    """
    rec_data = {
        "name": "test recipe",
        "prep_time": "5",
        "cook_time": "5",
        "servings": "1",
        "ingredients": ["garlic", "onion"],
        "directions": ["cook"],
        "notes": ["this is a test"],
        "tags": ["test"],
    }
    find = mocker.patch.object(AccountUC, "find_user_by_id")
    find.return_value = "FOUND"
    vm = mocker.patch.object(AddViewModel, "__call__")
    rec = mocker.patch.object(RecipeUC, "create_recipe")
    rec.return_value = testrecipe(**rec_data)
    with flask_app.test_request_context(path="/recipe/add", data=rec_data):
        resp: Response = recipe_views.recipe_add_post()
    assert resp.location in "/recipe/view/12345"


def test_recipe_add_post_loggedin_Notcreated(mocker, testrecipe):
    """
    GIVEN a logged-in user
    WHEN posting to /recipe/add but recipe is not created in DB
    THEN no errors and user stays on recipe/add page
    """
    rec_data = {
        "name": "test recipe",
        "prep_time": "5",
        "cook_time": "5",
        "servings": "1",
        "ingredients": ["garlic", "onion"],
        "directions": ["cook"],
        "notes": ["this is a test"],
        "tags": ["test"],
    }
    find = mocker.patch.object(AccountUC, "find_user_by_id")
    find.return_value = "FOUND"
    vm = mocker.patch.object(AddViewModel, "__call__")
    rec = mocker.patch.object(RecipeUC, "create_recipe")
    rec.return_value = None
    with flask_app.test_request_context(path="/recipe/add", data=rec_data):
        resp: Response = recipe_views.recipe_add_post()
    assert resp.location is None


#################### Recipe Editing #########################

def test_recipe_edit_get_loggedin(mocker):
    """
    GIVEN a logged-in user
    THEN navigating to /recipe/edit/<recipe_id>
    THEN assert no errors and stays on edit page
    """
    find = mocker.patch.object(AccountUC, "find_user_by_id")
    find.return_value = "FOUND"
    vm = mocker.patch.object(EditViewModel, "__call__")
    rec = mocker.patch.object(RecipeUC, "find_recipe_by_id")
    with flask_app.test_request_context(path="/recipe/edit/<recipe_id>", data=None):
        resp: Response = recipe_views.recipe_edit_get("12345")
    assert resp.location is None


def test_recipe_edit_get_loggedout(mocker):
    """
    GIVEN a logged-out or unregistered user
    WHEN attempting to navigate to /recipe/edit/<recipe_id>
    THEN assert redirected to login page
    """
    find = mocker.patch.object(AccountUC, "find_user_by_id")
    find.return_value = None
    vm = mocker.patch.object(EditViewModel, "__call__")
    with flask_app.test_request_context(path="/recipe/edit/<recipe_id>", data=None):
        resp: Response = recipe_views.recipe_edit_get("12345")
    assert resp.location in ("/account/login", "/login")


def test_recipe_edit_post_loggedin(mocker, testrecipe):
    """
    GIVEN a logged-in user
    WHEN posting to /recipe/edit/<recipe_id>
    THEN no errors and redirected to recipe/view/<recipe_id> page
    """
    rec_data = {
        "name": "test recipe",
        "prep_time": "5",
        "cook_time": "5",
        "servings": "1",
        "ingredients": ["garlic", "onion"],
        "directions": ["cook"],
        "notes": ["this is a test"],
        "tags": ["test"],
    }
    find = mocker.patch.object(AccountUC, "find_user_by_id")
    find.return_value = "FOUND"
    vm = mocker.patch.object(AddViewModel, "__call__")
    rec = mocker.patch.object(RecipeUC, "edit_recipe")
    rec.return_value = testrecipe(**rec_data)
    with flask_app.test_request_context(path="/recipe/add", data=rec_data):
        resp: Response = recipe_views.recipe_edit_post("12345")
    assert resp.location in "/recipe/view/12345"


def test_recipe_edit_post_loggedout(mocker):
    """
    GIVEN a logged-out or unregistered user
    WHEN attempting to post to /recipe/edit/<recipe_id>
    THEN assert redirected to login page
    """
    rec_data = {
        "name": "test recipe",
        "prep_time": "5",
        "cook_time": "5",
        "servings": "1",
        "ingredients": ["garlic", "onion"],
        "directions": ["cook"],
        "notes": ["this is a test"],
        "tags": ["test"],
    }
    find = mocker.patch.object(AccountUC, "find_user_by_id")
    find.return_value = None
    vm = mocker.patch.object(AddViewModel, "__call__")
    rec = mocker.patch.object(RecipeUC, "__call__")
    rec.return_value.create_recipe.return_value = "CREATED"
    with flask_app.test_request_context(path="/recipe/edit/<recipe_id>", data=rec_data):
        resp: Response = recipe_views.recipe_edit_post("12345")
    assert resp.location in ("/login", "/account/login")


#################### Recipe Deleting ########################

def test_recipe_delete_get_loggedin_goodrecipeID(mocker):
    """
    GIVEN a logged-in user
    THEN navigating to /recipe/delete/<recipe_id>
    THEN assert no errors and goes to correct page
    """
    find = mocker.patch.object(AccountUC, "find_user_by_id")
    find.return_value = "FOUND"
    vm = mocker.patch.object(DeleteViewModel, "__call__")
    rec = mocker.patch.object(RecipeUC, "find_recipe_by_id")
    rec.return_value = "FOUND"
    with flask_app.test_request_context(path="/recipe/delete/<recipe_id>", data=None):
        resp: Response = recipe_views.recipe_delete_get("12345")
    assert resp.location is None
    #assert vm.error is None


def test_recipe_delete_get_loggedin_badrecipeID(mocker):
    """
    GIVEN a logged-in user
    THEN navigating to /recipe/delete/<recipe_id>
    THEN assert no errors and goes to correct page
    """
    find = mocker.patch.object(AccountUC, "find_user_by_id")
    find.return_value = "FOUND"
    vm = mocker.patch.object(DeleteViewModel, "__call__")
    rec = mocker.patch.object(RecipeUC, "find_recipe_by_id")
    rec.return_value = None
    with flask_app.test_request_context(path="/recipe/delete/<recipe_id>", data=None):
        resp: Response = recipe_views.recipe_delete_get("12345")
    assert resp.location is None
    #assert vm.error == "Recipe Not Found"


def test_recipe_delete_get_loggedout(mocker):
    """
    GIVEN a logged-out or unregistered user
    WHEN attempting to navigate to /recipe/delete/<recipe_id>
    THEN assert redirected to login page
    """
    find = mocker.patch.object(AccountUC, "find_user_by_id")
    find.return_value = None
    vm = mocker.patch.object(DeleteViewModel, "__call__")
    rec = mocker.patch.object(RecipeUC, "find_recipe_by_id")
    rec.return_value = None
    with flask_app.test_request_context(path="/recipe/delete/<recipe_id>", data=None):
        resp: Response = recipe_views.recipe_delete_get("12345")
    assert resp.location in ("/account/login", "/login")


def test_recipe_delete_post_loggedin(mocker):
    """
    GIVEN a logged-in user
    WHEN navigating to to /recipe/delete/<recipe_id>
    THEN assert redirected to index after deleting the recipe
    """
    find = mocker.patch.object(AccountUC, "find_user_by_id")
    find.return_value = "FOUND"
    vm = mocker.patch.object(DeleteViewModel, "__call__")
    res = mocker.patch.object(RecipeUC, "delete_recipe")
    rec = mocker.patch.object(RecipeUC, "get_all_recipes")
    tags = mocker.patch.object(RecipeUC, "get_tags")
    with flask_app.test_request_context(path="/recipe/delete/<recipe_id>", data=None):
        resp: Response = recipe_views.recipe_delete_post("12345")
    assert resp.location is None


def test_recipe_delete_post_loggedout(mocker):
    """
    GIVEN a logged-out or unregistered user
    WHEN attempting to navigate to /recipe/delete/<recipe_id>
    THEN assert redirected to login page
    """
    find = mocker.patch.object(AccountUC, "find_user_by_id")
    find.return_value = None
    vm = mocker.patch.object(DeleteViewModel, "__call__")
    rec = mocker.patch.object(RecipeUC, "delete_recipe")
    rec.return_value = None
    with flask_app.test_request_context(path="/recipe/delete/<recipe_id>", data=None):
        resp: Response = recipe_views.recipe_delete_post("12345")
    assert resp.location in ("/account/login", "/login")

#################### Recipes with... ########################

def test_recipes_with_tags(mocker, testrecipe):
    """
    GIVEN recipes with tags in the DB
    WHEN navigating to /recipe/tag/<tags>
    THEN assert no errors
    """
    rec = mocker.patch.object(RecipeUC, "find_recipes_by_tag")
    rec.return_value = None
    with flask_app.test_request_context(path="/recipe/tag/<tags>", data=None):
        resp: Response = recipe_views.recipes_with_tags("test")
    assert resp.status_code == 200


def test_recipes_deleted(mocker):
    """
    GIVEN recipes in the DB and a logged-in user
    WHEN requesting to view /recipe/deleted
    THEN assert "Not Implemented" at the moment
    """
    rec = mocker.patch.object(RecipeUC, "get_all_recipes")
    rec.return_value = None
    with flask_app.test_request_context(path="/recipe/deleted", data=None):
        resp: Response = recipe_views.recipes_deleted()
    assert resp == "Not Implemented... yet"


def test_recipes_recently_added(mocker):
    """
    GIVEN recipes in the DB
    WHEN when navigating to recipes/recent
    THEN assert "Not Implemented" at the moment
    """
    with flask_app.test_request_context(path="/recipe/recent", data=None):
        resp: Response = recipe_views.recipes_recently_added()
    assert resp.location is None


def test_recipes_favorite(mocker):
    """
    GIVEN recipes in the DB
    WHEN when navigating to recipes/favorites
    THEN assert "Not Implemented" at the moment
    """
    with flask_app.test_request_context(path="/recipe/favorites", data=None):
        resp: Response = recipe_views.recipes_favorite()
    assert resp.location is None


def test_recipes_random(mocker):
    """
    GIVEN recipes in the DB
    WHEN when navigating to recipes/random
    THEN assert "Not Implemented" at the moment
    """
    with flask_app.test_request_context(path="/recipe/random", data=None):
        resp: Response = recipe_views.recipes_random()
    assert resp.location is None
