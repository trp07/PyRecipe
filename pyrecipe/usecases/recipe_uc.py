"""Use Cases for recipe-related logic."""

from typing import Optional
from typing import List
from pyrecipe.storage.mongo import MongoDriver


def get_all_recipes(deleted=None) -> List["RecipeModel"]:
    """Get all recipes in database."""
    if deleted == False:
        recipes = MongoDriver.recipes_active()
    elif deleted == True:
        recipes = MongoDriver.recipes_deleted()
    else:
        recipes = MongoDriver.recipes_all()
    return recipes


def find_recipe_by_id(recipe_id: str) -> Optional["RecipeModel"]:
    """Get specific recipe by id in database."""
    recipe = MongoDriver.recipe_find_by_id(recipe_id)
    return recipe


def create_recipe(
    name: str,
    prep_time: int,
    cook_time: int,
    servings: int,
    ingredients: List["ingredients"],
    directions: List["directions"],
    tags: List["tags"] = [],
    notes: List["notes"] = [],
) -> "RecipeModel":
    """Create a recipe in the database and return it."""
    recipe = MongoDriver.recipe_create(
        name=name,
        prep_time=prep_time,
        cook_time=cook_time,
        servings=servings,
        ingredients=ingredients,
        directions=directions,
        tags=tags,
        notes=notes,
    )
    return recipe


def find_recipes_by_tag(tags: List[str]) -> List["RecipeModel"]:
    """Find recipes with the given tags."""
    recipes = MongoDriver.recipes_find_by_tag(tags)
    return recipes


def get_tags() -> List[str]:
    """Get all the unique tags in the DB."""
    tags = MongoDriver.recipes_get_tags()
    return tags
