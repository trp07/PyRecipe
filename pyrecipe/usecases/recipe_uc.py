"""Use Cases for recipe-related logic."""

import datetime
import pathlib
from typing import Optional
from typing import List

from pyrecipe.services import export
from pyrecipe.files import FILESDIR


class RecipeUC:
    """Use Cases for recipe-related logic."""

    def __init__(self, db_driver):
        self._driver = db_driver

    def get_all_recipes(self, deleted=None) -> List["RecipeModel"]:
        """Get all recipes in database."""
        if deleted == False:
            recipes = self._driver.recipes_active()
        elif deleted == True:
            recipes = self._driver.recipes_deleted()
        else:
            recipes = self._driver.recipes_all()
        return recipes

    def find_recipe_by_id(self, recipe_id: str) -> Optional["RecipeModel"]:
        """Get specific recipe by id in database."""
        recipe = self._driver.recipe_find_by_id(recipe_id)
        return recipe

    def create_recipe(
        self,
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
        recipe = self._driver.recipe_create(
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

    def find_recipes_by_tag(self, tags: List[str]) -> List["RecipeModel"]:
        """Find recipes with the given tags."""
        recipes = self._driver.recipes_find_by_tag(tags)
        return recipes

    def get_tags(self) -> List[str]:
        """Get all the unique tags in the DB."""
        tags = self._driver.recipes_get_tags()
        return tags

    def edit_recipe(
        self,
        _id: str,
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
        recipe = self._driver.recipe_edit(
            _id=_id,
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

    def delete_recipe(self, recipe_id: str) -> int:
        """Marks the recipe as deleted."""
        return self._driver.recipe_delete(recipe_id)

    def recipes_search(self, text: str) -> Optional["RecipeModel"]:
        """Return a list of recipes that match the supplied search string."""
        name_search = self._driver.recipes_find_by_name(text)
        text_search = self._driver.recipes_search(text)
        return name_search + text_search

    def export_recipe(self, recipe_id: str) -> pathlib.Path:
        """
        Export the given recipe to a pdf and return the filepath of the pdf.
        If the file already exists because it was previously exported and it wasn't
        modified since the last export, then return the file instead of recreating
        it.
        """
        recipe = self.find_recipe_by_id(recipe_id)

        filename = recipe_id
        filename += "_"
        filename += datetime.datetime.strftime(recipe.last_modified_date, "%Y-%m-%d_%H-%M-%Sutc")
        filename += ".pdf"

        filepath = FILESDIR.joinpath("exports/" + filename)

        if filepath.is_file():
            result = filepath
        else:
            result = export.export_to_pdf(recipe, filename)

        return result
