from pyrecipe.app.viewmodels.shared import ViewModelBase


class AboutViewModel(ViewModelBase):
    """Viewmodel used for the /about view."""

    def __init__(self):
        super().__init__()
