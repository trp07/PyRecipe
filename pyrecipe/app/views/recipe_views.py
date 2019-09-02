"""
Views specific to viewing Recipes.
"""

from collections.abc import MutableSequence
from typing import List

import flask

from pyrecipe.frontend import TEMPLATESDIR
from pyrecipe.static import STATICDIR
from pyrecipe.app.helpers.view_modifiers import response
from pyrecipe.storage import Recipe


blueprint = flask.Blueprint(
    "recipe", __name__, template_folder=str(TEMPLATESDIR), static_folder=str(STATICDIR)
)


@blueprint.route("/recipe")
def recipes_all():
    """
    Routing required to view all recipes.

    :returns: all recipes where recipe.deleted==False.
    """
    recipes = [r for r in Recipe.objects() if r.deleted == False]
    return "Not Implemented... yet"


@blueprint.route("/recipe/view/<recipe_id>")
@response(template_file="recipe/recipe.html")
def recipe_view(recipe_id: str):
    """
    Routing required to view a recipe's details.

    :param recipe_id: (str) the DB id of the recipe.

    :returns: recipe or 404 if recipe is not found.
    """
    recipe = Recipe.objects().filter(id=recipe_id).first()
    if not recipe:
        flask.abort(404)
    return {"recipe": recipe}


@blueprint.route("/recipe/add", methods=["GET"])
def recipe_add_get():
    pass


@blueprint.route("/recipe/add", methods=["POST"])
def recipe_add_post():
    return "Not Implemented... yet"


@blueprint.route("/recipe/edit/<recipe_id>", methods=["GET"])
def recipe_edit_get():
    return "Not Implemented... yet"


@blueprint.route("/recipe/edit/<recipe_id>", methods=["POST"])
def recipe_edit_post():
    return "Not Implemented... yet"


@blueprint.route("/recipe/tag/<tags>")
@response(template_file="recipe/tag.html")
def recipes_with_tags(tags: List[str]):
    """
    Routing required to view recipes with a given tag.

    :param recipe_id: (str) the DB id of the recipe.

    :returns: recipe or 404 if recipe is not found.
    """
    if not isinstance(tags, MutableSequence):
        tags = [tags]
    recipes = Recipe.find_recipes_by_tag(tags)
    return {"recipes": recipes}


@blueprint.route("/recipe/deleted")
def recipes_deleted(username: str):
    """
    Routing required to view recipes that have been deleted.

    :returns: recipes where recipe.deleted==True.
    """
    recipes = [r for r in Recipe.objects() if r.deleted == True]
    return "Not Implemented... yet"
