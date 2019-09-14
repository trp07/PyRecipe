from pyrecipe.app.viewmodels.shared import ViewModelBase
from pyrecipe.storage.user import User


class LoginViewModel(ViewModelBase):
    """Viewmodel used for the /account/login view."""
    def __init__(self):
        super().__init__()
        self.email = self.request_dict.email.lower().strip()
        self.password = self.request_dict.password.strip()

    def validate(self):
        if not self.email or not self.email.strip():
            self.error = "Please enter an email address."
        elif not self.password:
            self.error = "Please enter a password."
        elif not User.login_user(self.email, self.password):
            self.error = "Username or password are incorrect."
