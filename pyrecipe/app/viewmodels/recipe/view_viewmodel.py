from pyrecipe.app.viewmodels.shared import ViewModelBase


class RecipeViewModel(ViewModelBase):
    """Viewmodel used for the /recipe/view/<recipe_id> view."""

    def __init__(self):
        super().__init__()
        self.recipe = None
