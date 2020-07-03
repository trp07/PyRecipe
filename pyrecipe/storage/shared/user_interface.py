"""
User Database Interface.

Abstract interface all DB Drivers will inherit from to
ensure consistent use and enable Interface Segragation.
"""

from abc import ABCMeta
from abc import abstractmethod
from typing import List
from typing import Optional


class UserDBInt(metaclass=ABCMeta):
    """
    Interface all DB USER interactions will be coded to to ensure
    consistency amongst DB implementations.  Methods should return
    UserModel's and not actual DB objects.
    """

    @abstractmethod
    def user_login(email: str, password: str) -> Optional["UserModel"]:
        """Login the user and return the user object."""
        pass

    @abstractmethod
    def user_create(name: str, email: str, password: str) -> "UserModel":
        """Create a new user and pass back the user object."""
        pass

    @abstractmethod
    def user_find_by_id(user_id: str) -> Optional["UserModel"]:
        """Retrieve user object by given id."""
        pass

    @abstractmethod
    def user_find_by_email(email: str) -> Optional["UserModel"]:
        """Retrieve user object by given email address."""
        pass

    @abstractmethod
    def users_list() -> List["UserModel"]:
        """List all registered users."""
        pass

    @abstractmethod
    def user_add_recipe(user: "UserModel", recipe: "RecipeModel") -> int:
        """Add a recipe to a user's collection."""
        pass

    @abstractmethod
    def user_set_password(user: "UserModel", password: str) -> int:
        """Allow user to change password."""
        pass
