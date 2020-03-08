from collections import namedtuple
from typing import List

from pyrecipe.app.viewmodels.shared import ViewModelBase
from pyrecipe.storage.recipe import Recipe
from pyrecipe.storage.user import User


class AddViewModel(ViewModelBase):
    """Viewmodel used for the /recipe/add view."""
    Ingredient = namedtuple("Ingredient", ["name", "quantity", "unit", "preparation"])

    def __init__(self):
        super().__init__()
        self.method = self.request.method
        self.path = self.request.path

    @property
    def ingredients(self) -> List["Ingredient"]:
        """Returns all ingredients passed in from user input."""
        num_ingredients = len(self.request.form.getlist("i_name"))
        names = self.request.form.getlist("i_name")
        quantities = self.request.form.getlist("i_quantity")
        units = self.request.form.getlist("i_unit")
        preparations = self.request.form.getlist("i_preparation")

        igrs = []
        for i in range(num_ingredients):
            try:
                unit = units[i]
            except IndexError:
                unit = ""

            try:
                prep = preparations[i]
            except IndexError:
                prep = ""

            igr = AddViewModel.Ingredient(names[i], quantities[i], unit, prep)
            igrs.append(igr)

        return igrs

    @property
    def tags(self) -> List["tags"]:
        """Returns all tags passed in from user input."""
        tags = [t.strip().lower() for t in self.request.form["tags"].split("\n") if t.strip()]
        if not tags:
            return []
        return list(set(tags))

    @property
    def directions(self) -> List["directions"]:
        """Returns all directions passed in from user input."""
        directions = [d.strip() for d in self.request.form["directions"].split("\n") if d.strip()]
        return directions

    @property
    def notes(self) -> List["notes"]:
        """Returns all notes passed in from user input."""
        notes = [n.strip() for n in self.request.form["notes"].split("\n") if n.strip()]
        return notes

    @property
    def prep_time(self) -> int:
        prep_time = self.request_dict.prep_time
        if prep_time == '':
            return 0
        else:
            return int(prep_time)

    @property
    def cook_time(self) -> int:
        cook_time = self.request_dict.cook_time
        if cook_time == '':
            return 0
        else:
            return int(cook_time)

    @property
    def servings(self) -> int:
        servings = self.request_dict.servings
        if servings == '':
            return 0
        else:
            return int(servings)

    @property
    def name(self) -> str:
        return self.request_dict.name

