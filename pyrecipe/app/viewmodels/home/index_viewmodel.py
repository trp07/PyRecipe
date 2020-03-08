from pyrecipe.app.viewmodels.shared import ViewModelBase
from pyrecipe.storage.user import User
from pyrecipe.storage.recipe import Recipe


class IndexViewModel(ViewModelBase):
    """Viewmodel used for the /index view."""

    def __init__(self):
        super().__init__()

    def validate(self):
        if not self.user:
            self.name = "Guest"
        else:
            self.name = self.user.name

    def get_recipes(self):
        self.recipes = [r for r in Recipe.objects() if r.deleted == False]
        self.tags = Recipe.get_tags()
