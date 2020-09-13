"""View controllers associated with recipe features."""

from collections.abc import MutableSequence
from typing import List

import flask
from flask import current_app

from pyrecipe.app.helpers.view_modifiers import response
from pyrecipe.app.helpers import request_dict
from pyrecipe.app.viewmodels.recipe import AddViewModel
from pyrecipe.app.viewmodels.recipe import EditViewModel
from pyrecipe.app.viewmodels.recipe import RecipeViewModel
from pyrecipe.frontend import TEMPLATESDIR
from pyrecipe.static import STATICDIR
from pyrecipe.usecases.recipe_uc import RecipeUC


blueprint = flask.Blueprint(
    "recipe", __name__, template_folder=str(TEMPLATESDIR), static_folder=str(STATICDIR)
)


#################### Recipe Viewing #########################


@blueprint.route("/recipe/all", methods=["GET"])
def recipes_all():
    """
    Routing required to view all recipes.

    :returns: all recipes where recipe.deleted==False.
    """
    uc = RecipeUC(current_app.config["DB_DRIVER"])
    recipes = uc.get_all_recipes(deleted=False)
    return "Not Implemented... yet"


@blueprint.route("/recipe/view/<recipe_id>", methods=["GET"])
@response(template_file="recipe/recipe.html")
def recipe_view(recipe_id: str):
    """
    Routing required to view a recipe's details.

    :param recipe_id: (str) the DB id of the recipe.

    :returns: recipe or 404 if recipe is not found.
    """
    vm = RecipeViewModel()
    uc = RecipeUC(current_app.config["DB_DRIVER"])
    vm.recipe = uc.find_recipe_by_id(recipe_id)
    if not vm.recipe:
        flask.abort(404)
    return vm.to_dict()


#################### Recipe Adding ##########################


@blueprint.route("/recipe/add", methods=["GET"])
@response(template_file="recipe/add_recipe.html")
def recipe_add_get():
    vm = AddViewModel()
    if not vm.user:
        return flask.redirect(flask.url_for("account.login_get"))
    return vm.to_dict()


@blueprint.route("/recipe/add", methods=["POST"])
@response(template_file="recipe/add_recipe.html")
def recipe_add_post():
    vm = AddViewModel()
    if not vm.user:
        return flask.redirect(flask.url_for("account.login_get"))

    uc = RecipeUC(current_app.config["DB_DRIVER"])
    recipe = uc.create_recipe(
        name=vm.name,
        prep_time=vm.prep_time,
        cook_time=vm.cook_time,
        servings=vm.servings,
        ingredients=vm.ingredients,
        directions=vm.directions,
        tags=vm.tags,
        notes=vm.notes,
    )
    if recipe:
        return flask.redirect(
            flask.url_for("recipe.recipe_view", recipe_id=str(recipe.id))
        )
    return vm.to_dict()


#################### Recipe Editing #########################


@blueprint.route("/recipe/edit/<recipe_id>", methods=["GET"])
@response(template_file="recipe/add_recipe.html")
def recipe_edit_get(recipe_id: str):
    vm = EditViewModel()
    if not vm.user:
        return flask.redirect(flask.url_for("account.login_get"))

    uc = RecipeUC(current_app.config["DB_DRIVER"])
    vm.recipe = uc.find_recipe_by_id(recipe_id)

    return {**vm.to_dict(), **vm.edit_form()}


@blueprint.route("/recipe/edit/<recipe_id>", methods=["POST"])
@response(template_file="recipe/add_recipe.html")
def recipe_edit_post(recipe_id: str):
    vm = AddViewModel()
    if not vm.user:
        return flask.redirect(flask.url_for("account.login_get"))

    uc = RecipeUC(current_app.config["DB_DRIVER"])
    recipe = uc.edit_recipe(
        _id=vm.path.split("/")[-1],
        name=vm.name,
        prep_time=vm.prep_time,
        cook_time=vm.cook_time,
        servings=vm.servings,
        ingredients=vm.ingredients,
        directions=vm.directions,
        tags=vm.tags,
        notes=vm.notes,
    )
    if recipe:
        return flask.redirect(
            flask.url_for("recipe.recipe_view", recipe_id=str(recipe.id))
        )
    return vm.to_dict()



#################### Recipes with... ########################


@blueprint.route("/recipe/tag/<tags>", methods=["GET"])
@response(template_file="recipe/tag.html")
def recipes_with_tags(tags: List[str]):
    """
    Routing required to view recipes with a given tag.

    :param recipe_id: (str) the DB id of the recipe.

    :returns: recipe or 404 if recipe is not found.
    """
    if not isinstance(tags, MutableSequence):
        tags = [tags]

    uc = RecipeUC(current_app.config["DB_DRIVER"])
    recipes = uc.find_recipes_by_tag(tags)
    return {"recipes": recipes}


@blueprint.route("/recipe/deleted", methods=["GET"])
def recipes_deleted():
    """
    Routing required to view recipes that have been marked as deleted.
    """
    uc = RecipeUC(current_app.config["DB_DRIVER"])
    recipes = uc.get_all_recipes(deleted=True)
    return "Not Implemented... yet"


@blueprint.route("/recipes/recent", methods=["GET"])
@blueprint.route("/recipes/recent/", methods=["GET"])
@blueprint.route("/recipes/recent/<num_rec>", methods=["GET"])
@response(template_file="recipe/recent_recipes.html")
def recipes_recently_added(num_rec: int = 10):
    """Show the num_rec most recently added recipes."""
    return {"error": "Not yet implemented!"}


@blueprint.route("/recipes/favorites", methods=["GET"])
@blueprint.route("/recipes/favorites/", methods=["GET"])
@blueprint.route("/recipes/favorites/<num_rec>", methods=["GET"])
@response(template_file="recipe/favorite_recipes.html")
def recipes_favorite(num_rec: int = 10):
    """Show the num_rec favorite recipes."""
    return {"error": "Not yet implemented!"}


@blueprint.route("/recipes/random", methods=["GET"])
@blueprint.route("/recipes/random/", methods=["GET"])
@blueprint.route("/recipes/random/<num_rec>", methods=["GET"])
@response(template_file="recipe/random_recipes.html")
def recipes_random(num_rec: int = 10):
    """Show the num_rec random recipes."""
    return {"error": "Not yet implemented!"}
