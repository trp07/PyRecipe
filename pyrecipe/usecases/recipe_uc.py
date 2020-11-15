"""Use Cases for recipe-related logic."""

from typing import Optional
from typing import List


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


    def delete_recipe(self, recipe_id:str) -> int:
        """Marks the recipe as deleted."""
        return self._driver.recipe_delete(recipe_id)
