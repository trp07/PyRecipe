"""
User Object Model.

Datastructure that encapsulates all required User object
attributes for delivery to usecases.
"""

from dataclasses import dataclass


@dataclass
class UserModel:
    """User data objects all DB records will be translated into."""

    _id: str
    name: str
    username: str
    email: str
    password_hash: str
    created_date: "datetime.datetime"
    last_modified_date: "datetime.datetime"
    recipe_ids: list
    shared_recipe_ids: list
    email_distros: dict

    @property
    def id(self) -> str:
        return self._id

    @classmethod
    def from_dict(cls, adict) -> "UserModel":
        return cls(**adict)

    def to_dict(self) -> dict:
        return self.__dict__
