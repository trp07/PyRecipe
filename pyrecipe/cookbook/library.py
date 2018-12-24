import abc

class LibraryInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    @staticmethod
    def find_recipe_by_name(name):
        """
        Library.find_recipe_by_name('Vietnamese Pork')

        :param name: A recipe name as a string.
        :return: A recipe object
        """
        raise NotImplementedError

    @abc.abstractmethod
    @staticmethod
    def find_recipes_by_field(tags=None, ingredients=None):
        """
        Library.find_recipes_by_field(tags=['mexican', 'hot'], ingredients=['pepper'])

        :param tags: A list of tags.
        :param ingredients: A list of ingredients.
        :returns: A list of recipe objects.
        """
        raise NotImplementedError

    @abc.abstractmethod
    @staticmethod
    def delete_recipe(recipe):
        """
        Library.delete_recipe(recipe)

        :param recipe: A recipe object.
        :returns: {'success': boolean, 'cached_until': datetime}
        """
        raise NotImplementedError

    @abc.abstractmethod
    @staticmethod
    def add_recipe(recipe):
        """
        Library.add_recipe(recipe)

        :param recipe: A recipe object.
        :return: {'success': boolean, 'recipe': recipe}
        """
        raise NotImplementedError

class TagsInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    @staticmethod
    def list():
        """
        Tags.list()

        :returns: A list of tags.
        """
        raise NotImplementedError

    @abc.abstractmethod
    @staticmethod
    def add(tag):
        """
        Tags.add(['hot', 'spicy'])

        :param tag: A list of strings.
        :return: Boolean based on success.
        """
        raise NotImplementedError

class IngredientsInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    @staticmethod
    def list():
        """
        Ingredients.list()

        :return: A list of ingredients.
        """
        raise NotImplementedError

    @abc.abstractmethod
    @staticmethod
    def add(ingredients: list):
        """
        Ingredients.add(['red pepper', 'green pepper'])
        :param ingredients:
        :return: Boolean based on success.
        """
        raise NotImplementedError
