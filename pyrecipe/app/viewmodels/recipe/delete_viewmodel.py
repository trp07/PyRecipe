from pyrecipe.app.viewmodels.shared import ViewModelBase


class DeleteViewModel(ViewModelBase):
    """Viewmodel used for the /recipe/delete view."""

    def __init__(self):
        super().__init__()
        self.method = self.request.method
        self.path = self.request.path
        self.recipe = None
        self.recipes = None
        self.tags = None
