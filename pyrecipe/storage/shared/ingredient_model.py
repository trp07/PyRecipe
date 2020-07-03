"""
Ingredient Object Model.

Datastructure that encapsulates all required Ingredient object
attributes for delivery to usecases.
"""

from dataclasses import dataclass


@dataclass
class IngredientModel:
    """Ingredient data objects all DB records will be translated into."""

    name: str
    quantity: str
    unit: str
    preparation: str

    @classmethod
    def from_dict(cls, adict) -> "IngredientModel":
        return cls(**adict)

    def to_dict(self) -> dict:
        return self.__dict__
