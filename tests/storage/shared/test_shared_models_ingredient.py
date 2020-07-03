import pytest

from pyrecipe.storage.shared import IngredientModel

####### globals #########

INGREDIENT = {
    "name": "garlic",
    "quantity": "1",
    "unit": "clove",
    "preparation": "minced",
}


###### test funcs #########

def test_ingredientmodel_init():
    """Verifies a IngredientModel is properly instantiated."""
    ingredient = IngredientModel(**INGREDIENT)
    assert ingredient.name == "garlic"
    assert ingredient.quantity == "1"
    assert ingredient.unit == "clove"
    assert ingredient.preparation == "minced"


def test_ingredientmodel_fromdict():
    """Verifies a IngredientModel is properly instantiated via the
    from_dict() method."""
    ingredient = IngredientModel.from_dict(INGREDIENT)
    assert ingredient.name == "garlic"
    assert ingredient.quantity == "1"
    assert ingredient.unit == "clove"
    assert ingredient.preparation == "minced"


def test_ingredientmodel_todict():
    """Verifies a properly formed dict is returned from the
    IngredientModel.to_dict() method."""
    ingredient = IngredientModel(**INGREDIENT)
    ingredient_dict = ingredient.to_dict()
    assert ingredient_dict == INGREDIENT
