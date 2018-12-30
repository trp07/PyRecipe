import abc


class RecipeInterface(metaclass=abc.ABCMeta):
    """
    A class for interacting with a Recipe instance
    """

    @abc.abstractmethod
    def copy_recipe(self, name: str):
        """
        Given a recipe instance, produce a copy of it with a modified name

        :param name: a string representing the new name
        :return: a Recipe instance with a modified name
        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete_recipe(self) -> bool:
        """
        Given a recipe instance, delete it from the library

        :return: Boolean, representing success or failure
        """
        raise NotImplementedError

    @abc.abstractmethod
    def restore_recipe(self) -> bool:
        """
        Given a recipe instance, restores a deleted recipe

        :return: Boolean, representing success or failure
        """
        raise NotImplementedError
