from pyrecipe.app.viewmodels.shared import ViewModelBase


class SearchViewModel(ViewModelBase):
    """Viewmodel used for the /recipe/search view."""

    def __init__(self):
        super().__init__()
        self.text = self.request_dict.search_text.strip()

    def validate(self):
        if not self.user:
            self.name = "Guest"
        else:
            self.name = self.user.name
