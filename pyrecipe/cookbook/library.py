import abc
from .recipe import Recipe


##############################################################################
# Interfaces
##############################################################################


class LibraryInterface(metaclass=abc.ABCMeta):
    """
    A class for interacting with the PyRecipe database.
    """

    @staticmethod
    @abc.abstractmethod
    def find_by_name(name: str) -> Recipe:
        """
        Library.find_recipe_by_name('Vietnamese Pork')

        :param name: A recipe name as a string.
        :return: A recipe object
        """
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def find_by_field(tags: list = None, ingredients: list = None) -> list:
        """
        Library.find_by_field(tags=['mexican', 'hot'], ingredients=['pepper'])

        :param tags: A list of tags.
        :param ingredients: A list of ingredients.
        :returns: A list of recipe objects.
        """
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def delete(recipe: Recipe) -> dict:
        """
        Library.delete(recipe)

        :param recipe: A recipe object.
        :returns: {'success': boolean, 'cached_until': datetime}
        """
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def add(recipe: Recipe) -> dict:
        """
        Library.add(recipe)

        :param recipe: A recipe object.
        :return: {'success': boolean, 'recipe': recipe}
        """
        raise NotImplementedError


class TagsInterface(metaclass=abc.ABCMeta):
    """
    A class for interacting with tags in the PyRecipe database.
    """

    @staticmethod
    @abc.abstractmethod
    def list() -> list:
        """
        Tags.list()

        :returns: A list of tags.
        """
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def add(tag) -> bool:
        """
        Tags.add(['hot', 'spicy'])

        :param tag: A list of strings.
        :return: Boolean based on success.
        """
        raise NotImplementedError


class IngredientsInterface(metaclass=abc.ABCMeta):
    """
    A class for interacting with ingredients in the PyRecipe database.
    """

    @staticmethod
    @abc.abstractmethod
    def list() -> list:
        """
        Ingredients.list()

        :return: A list of ingredients.
        """
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def add(ingredients: list) -> bool:
        """
        Ingredients.add(['red pepper', 'green pepper'])

        :param ingredients:
        :return: Boolean based on success.
        """
        raise NotImplementedError


##############################################################################
# Implementations
##############################################################################


class Library(LibraryInterface):
    pass


class Tags(TagsInterface):
    pass


class Ingredients(IngredientsInterface):
    pass
