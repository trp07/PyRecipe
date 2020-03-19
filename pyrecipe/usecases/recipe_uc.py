"""Use Cases for recipe-related logic."""

from typing import Optional
from typing import List
from pyrecipe.storage import Recipe


def get_all_recipes() -> List[Recipe]:
    """Get all recipes in database"""
    recipes = Recipe.all_recipes()
    return recipes


def find_recipe_by_id(recipe_id: str) -> Optional["Recipe"]:
    """Get specific recipe by id in database"""
    recipe = Recipe.find_recipe_by_id(recipe_id)
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
    ) -> Recipe:
    """Create a recipe in the database and return it."""
    recipe = Recipe.create_recipe(
        name=name,
        prep_time=prep_time,
        cook_time=cook_time,
        servings=servings,
        ingredients=ingredients,
        directions=directions,
        tags=tags,
        notes=notes)
    return recipe


def find_recipes_by_tag(tags: List[str]) -> List[Recipe]:
    """Find recipes with the given tags"""
    recipes = Recipe.find_recipes_by_tag(tags)
    return recipes
