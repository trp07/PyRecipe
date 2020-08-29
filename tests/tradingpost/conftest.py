"""Fixtures and config items for testing this module."""

import pytest


class Recipe:
    def __init__(
        self, _id, name, prep_time, cook_time, servings, ingredients, directions, notes
    ):
        self.id = _id
        self.name = name
        self.prep_time = prep_time
        self.cook_time = cook_time
        self.servings = servings
        self.ingredients = ingredients
        self.directions = directions
        self.notes = notes


@pytest.fixture(scope="function")
def get_recipe():
    r1 = Recipe(
        _id=1,
        name="test1",
        prep_time=5,
        cook_time=10,
        servings=4,
        ingredients=[
            "garlic, 1 clove minced",
            "onion, 1 whole chopped"
        ],
        directions=["step1", "step2"],
        notes=["some notes"],
    )

    r2 = Recipe(
        _id=2,
        name="test2",
        prep_time=5,
        cook_time=10,
        servings=4,
        ingredients=[
            "garlic, 1 clove minced",
            "onion, 1 whole chopped"
        ],
        directions=["step1", "step2"],
        notes=["some notes"],
    )

    yield [r1, r2]
