from typing import List

from pyrecipe.app.viewmodels.shared import ViewModelBase


class EditViewModel(ViewModelBase):
    """Viewmodel used for the /recipe/edit view."""

    def __init__(self):
        super().__init__()
        self.method = self.request.method
        self.path = self.request.path
        self.recipe = None

    @property
    def _id(self) -> str:
        if self.method=="GET" and self.recipe:
            return str(self.recipe._id)

    @property
    def name(self) -> str:
        if self.method=="GET" and self.recipe:
            return self.recipe.name

    @property
    def prep_time(self) -> int:
        if self.method=="GET" and self.recipe:
            return int(self.recipe.prep_time)

    @property
    def cook_time(self) -> int:
        if self.method=="GET" and self.recipe:
            return int(self.recipe.cook_time)

    @property
    def servings(self) -> str:
        if self.method=="GET" and self.recipe:
            return self.recipe.servings

    @property
    def ingredients(self) -> List[str]:
        if self.method=="GET" and self.recipe:
            igrs = ""
            for i in self.recipe.ingredients:
                igrs += i
                igrs += "\n"
            return igrs

    @property
    def directions(self) -> List[str]:
        if self.method=="GET" and self.recipe:
            dirs = ""
            for d in self.recipe.directions:
                dirs += d
                dirs += "\n"
            return dirs

    @property
    def notes(self) -> List[str]:
        if self.method=="GET" and self.recipe:
            nts = ""
            for n in self.recipe.notes:
                nts += n
                nts += "\n"
            return nts

    @property
    def tags(self) -> List[str]:
        if self.method=="GET" and self.recipe:
            tgs = ""
            for t in self.recipe.tags:
                tgs += t
                tgs += "\n"
            return tgs

    def edit_form(self) -> dict:
        return {
            "_id": self._id,
            "name": self.name,
            "prep_time": self.prep_time,
            "cook_time": self.cook_time,
            "servings": self.servings,
            "ingredients": self.ingredients,
            "directions": self.directions,
            "notes": self.notes,
            "tags": self.tags,
        }
