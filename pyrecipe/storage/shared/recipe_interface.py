"""
Recipe Database Interface.

Abstract interface all DB Drivers will inherit from to
ensure consistent use and enable Interface Segragation.
"""

from abc import ABCMeta
from abc import abstractmethod
from typing import Optional
from typing import List


class RecipeDBInt(metaclass=ABCMeta):
    """
    Interface all DB RECIPE interactions will be coded to to ensure
    consistency amongst DB implementations.  Methods should return
    RecipeModel's and not actual DB objects.
    """

    @abstractmethod
    def recipe_create(**kwargs) -> "RecipeModel":
        """Create a recipe and save it in DB."""
        pass

    @abstractmethod
    def recipe_edit(**kwargs) -> "RecipeModel":
        """Wholescale edit a recipe's information and save it in DB."""
        pass

    @abstractmethod
    def recipe_find_by_id(recipe_id: str) -> Optional["RecipeModel"]:
        """Find recipe in DB by given id."""
        pass

    def recipes_find_by_name(search_string: str) -> Optional["RecipeModel"]:
        """Find list of recipes in DB by given name."""
        pass

    @abstractmethod
    def recipes_find_by_tag(tags: List[str]) -> Optional["RecipeModel"]:
        """Find all recipes with given tag."""
        pass

    @abstractmethod
    def recipes_get_tags() -> List["tags"]:
        """Return a list of all distinct tags in recipe DB."""
        pass

    @abstractmethod
    def recipes_all() -> List["RecipeModel"]:
        """Return all Recipes in the DB."""
        pass

    @abstractmethod
    def recipes_active() -> List["RecipeModel"]:
        """Return all Recipes in the DB not marked as deleted."""
        pass

    @abstractmethod
    def recipes_deleted() -> Optional["RecipeModel"]:
        """Return all Recipes in the DB marked as deleted."""
        pass

    @abstractmethod
    def recipe_copy(recipe: "Recipe") -> "RecipeModel":
        """Return a copy of the given recipe."""
        pass

    @abstractmethod
    def recipe_add_tag(recipe: "RecipeModel", tag: str) -> int:
        """Add a tag to a given recipe."""
        pass

    @abstractmethod
    def recipe_delete_tag(recipe: "RecipeModel", tag: str) -> int:
        """Delete a given tag from a recipe."""
        pass

    @abstractmethod
    def recipe_mark_made(recipe: "RecipeModel", date: "datetime.dateime") -> int:
        """Add a date the recipe was made."""
        pass

    @abstractmethod
    def recipe_delete(recipe: "RecipeModel") -> int:
        """Mark the given recipe as deleted."""
        pass

    @abstractmethod
    def recipes_search(text: str) -> Optional["RecipeModel"]:
        """Return a list of recipes that match the search string."""
        pass
