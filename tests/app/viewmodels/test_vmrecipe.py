"""Tests for pyrecipe/app/viewmodels."""

from flask import Response

from pyrecipe.usecases.account_uc import AccountUC
from pyrecipe.usecases.recipe_uc import RecipeUC
from pyrecipe.app.viewmodels.recipe import AddViewModel
from pyrecipe.app.viewmodels.recipe import EditViewModel
from pyrecipe.app.viewmodels.recipe import RecipeViewModel
from pyrecipe.app import app as flask_app


def test_recipevm(mocker):
    """
    GIVEN a blank request and no recipe yet to pass into the model
    WHEN a request is passed through the RecipeViewModel
    THEN assert no errors are received
    """
    target = mocker.patch.object(AccountUC, "find_user_by_id")
    target.return_value = None
    with flask_app.test_request_context(path="/recipe/view/<recipe_id>", data=None):
        vm = RecipeViewModel()

    vm.to_dict()
    assert vm.error is None
    assert vm.recipe is None


def test_addvm(mocker):
    """
    GIVEN a recipe to add
    WHEN submitted through the AddViewModel
    THEN assert it is created properly.

    NOTES: cannot check ingredients, directions, and notes in this test
    since it requires a in-depth integration test to pull our form data from
    request.form.  These will be tested in another test.
    """
    form_data = {
        "name": "oatmeal",
        "servings": "4",
        "cook_time": "30",
        "prep_time": "2",
        "notes": ["tastes good with almond butter mixed in"],
        "directions": [
            "combine oatmeal and water in instant pot",
            "set on manual for 4 minutes",
            "let sit for 20 minutes after the 4-minute pressure cook",
        ],
        "tags": ["breakfast", "easy"],
        "ingredients": [
            "steel cut oatmeal, 2 cups",
            "water, 5 cups",
        ],
    }

    target = mocker.patch.object(AccountUC, "find_user_by_id")
    target.return_value = None
    with flask_app.test_request_context(path="/recipe/add", data=form_data):
        vm = AddViewModel()

    assert vm.name == "oatmeal"
    assert vm.servings == 4
    assert vm.cook_time == 30
    assert vm.prep_time == 2


def test_editvm(mocker, testrecipe):
    """
    GIVEN a request to /recipe/edit/<recipe_id>
    WHEN data is passed through the viewmodel
    THEN assert there are no errors and the proper viewmodel is formed
    """
    target = mocker.patch.object(AccountUC, "find_user_by_id")
    target.return_value = None
    with flask_app.test_request_context(path="/recipe/edit/<recipe_id>", data=None):
        vm = EditViewModel()
        vm.recipe = testrecipe(
                name="tester", prep_time=5, cook_time=10, servings=4,
                ingredients=["igr1", "igr2"], directions=["do this", "do that"],
                notes=["sub igr3 for igr2"], tags=["t1", "t2"]
            )
    edit_form = vm.edit_form()
    assert edit_form["_id"] == "12345"
    assert edit_form["name"] == "tester"
    assert edit_form["prep_time"] == 5
    assert edit_form["cook_time"] == 10
    assert edit_form["servings"] == 4
    assert edit_form["ingredients"] == "igr1\nigr2\n"
    assert edit_form["directions"] == "do this\ndo that\n"
    assert edit_form["notes"] == "sub igr3 for igr2\n"
    assert edit_form["tags"] == "t1\nt2\n"
    assert vm.error is None
