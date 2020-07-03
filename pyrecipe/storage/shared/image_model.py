"""
Image Object Model.

Datastructure that encapsulates all required Image object
attributes for delivery to usecases.
"""

from dataclasses import dataclass


@dataclass
class ImageModel:
    """Ingredient data objects all DB records will be translated into."""

    recipe_id: str
    filepath: str
    description: str

    @classmethod
    def from_dict(cls, adict) -> "IngredientModel":
        return cls(**adict)

    def to_dict(self) -> dict:
        return self.__dict__
