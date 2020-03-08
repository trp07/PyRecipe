from collections import namedtuple
from typing import List

from pyrecipe.app.viewmodels.shared import ViewModelBase
from pyrecipe.storage.recipe import Recipe
from pyrecipe.storage.user import User


class EditViewModel(ViewModelBase):
    """Viewmodel used for the /recipe/edit view."""

    Ingredient = namedtuple("Ingredient", ["name", "quantity", "unit", "preparation"])

    def __init__(self):
        super().__init__()
        self.method = self.request.method
        self.path = self.request.path
        self.recipe = Recipe.find_recipe_by_id(self.path.split("/")[-1])
