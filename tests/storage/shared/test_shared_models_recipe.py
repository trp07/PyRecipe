import datetime

import pytest

from pyrecipe.storage.shared import RecipeModel

####### globals #########

DATE = datetime.datetime.utcnow()

RECIPE = {
    "_id": "123456",
    "name": "test recipe",
    "num_ingredients": 5,
    "directions": ["step 1", "step 2"],
    "prep_time": 10,
    "cook_time": 20,
    "servings": 4,
    "tags": ["spicy", "tester"],
    "notes": ["note 1", "note 2"],
    "rating": 3.5,
    "favorite": True,
    "when_made": DATE,
    "deleted": False,
    "created_date": DATE,
    "last_modified_date": DATE,
    "ingredients": ["one", "two"],
    "images": ["path to image"],
}


###### test funcs #########

def test_recipemodel_init():
    """Verifies a RecipeModel is properly instantiated."""
    recipe = RecipeModel(**RECIPE)
    assert recipe.id == "123456"
    assert recipe.name == "test recipe"
    assert recipe.num_ingredients == 5
    assert recipe.directions == ["step 1", "step 2"]
    assert recipe.prep_time == 10
    assert recipe.cook_time == 20
    assert recipe.servings == 4
    assert recipe.tags == ["spicy", "tester"]
    assert recipe.notes == ["note 1", "note 2"]
    assert recipe.rating == 3.5
    assert recipe.favorite == True
    assert recipe.when_made == DATE
    assert recipe.deleted == False
    assert recipe.created_date == DATE
    assert recipe.last_modified_date == DATE
    assert recipe.ingredients == ["one", "two"]
    assert recipe.images == ["path to image"]


def test_recipemodel_fromdict():
    """Verifies a RecipeModel is properly instantiated via the
    from_dict() method."""
    recipe = RecipeModel.from_dict(RECIPE)
    assert recipe.id == "123456"
    assert recipe.name == "test recipe"
    assert recipe.num_ingredients == 5
    assert recipe.directions == ["step 1", "step 2"]
    assert recipe.prep_time == 10
    assert recipe.cook_time == 20
    assert recipe.servings == 4
    assert recipe.tags == ["spicy", "tester"]
    assert recipe.notes == ["note 1", "note 2"]
    assert recipe.rating == 3.5
    assert recipe.favorite == True
    assert recipe.when_made == DATE
    assert recipe.deleted == False
    assert recipe.created_date == DATE
    assert recipe.last_modified_date == DATE
    assert recipe.ingredients == ["one", "two"]
    assert recipe.images == ["path to image"]


def test_recipemodel_todict():
    """Verifies a properly formed dict is returned from the
    RecipeModel.to_dict() method."""
    recipe = RecipeModel(**RECIPE)
    recipe_dict = recipe.to_dict()
    assert recipe_dict == RECIPE
