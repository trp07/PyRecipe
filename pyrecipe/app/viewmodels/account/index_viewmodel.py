from pyrecipe.app.viewmodels.shared import ViewModelBase
from pyrecipe.storage.user import User


class IndexViewModel(ViewModelBase):
    """Viewmodel used for the /account/ view."""
    def __init__(self):
        super().__init__()
        self.user = User.find_user_by_id(self.user_id)
