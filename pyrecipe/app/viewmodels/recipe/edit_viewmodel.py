from collections import namedtuple
from typing import List

from pyrecipe.app.viewmodels.shared import ViewModelBase


class EditViewModel(ViewModelBase):
    """Viewmodel used for the /recipe/edit view."""

    Ingredient = namedtuple("Ingredient", ["name", "quantity", "unit", "preparation"])

    def __init__(self):
        super().__init__()
        self.method = self.request.method
        self.path = self.request.path
