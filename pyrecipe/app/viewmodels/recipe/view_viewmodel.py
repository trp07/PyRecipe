from pyrecipe.app.viewmodels.shared import ViewModelBase
from pyrecipe.usecases import recipe_uc


class RecipeViewModel(ViewModelBase):
    """Viewmodel used for the /recipe/view/<recipe_id> view."""

    def __init__(self, recipe_id):
        super().__init__()
        self.recipe = recipe_uc.find_recipe_by_id(recipe_id)

