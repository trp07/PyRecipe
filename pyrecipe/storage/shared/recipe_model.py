"""
Recipe Object Model.

Datastructure that encapsulates all required Recipe object
attributes for delivery to usecases.
"""

from dataclasses import dataclass


@dataclass
class RecipeModel:
    """Recipe data objects all DB records will be translated into."""

    _id: str
    name: str
    num_ingredients: int
    directions: list
    prep_time: float
    cook_time: float
    servings: int
    tags: list
    notes: list
    rating: float
    favorite: bool
    when_made: list
    deleted: bool
    created_date: "datetime.datetime"
    last_modified_date: "datetime.datetime"
    ingredients: list
    images: list

    @property
    def id(self) -> str:
        return self._id

    @classmethod
    def from_dict(cls, adict) -> "RecipeModel":
        return cls(**adict)

    def to_dict(self) -> dict:
        return self.__dict__
