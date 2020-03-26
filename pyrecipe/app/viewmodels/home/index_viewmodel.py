from pyrecipe.app.viewmodels.shared import ViewModelBase
from pyrecipe.usecases import account_uc
from pyrecipe.usecases import recipe_uc


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
        self.recipes = recipe_uc.get_all_recipes(deleted=False)
        self.tags = recipe_uc.get_tags()
