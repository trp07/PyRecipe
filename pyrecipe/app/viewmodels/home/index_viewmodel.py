from pyrecipe.app.viewmodels.shared import ViewModelBase


class IndexViewModel(ViewModelBase):
    """Viewmodel used for the /index view."""

    def __init__(self):
        super().__init__()

    def validate(self):
        if not self.user:
            self.name = "Guest"
        else:
            self.name = self.user.name
