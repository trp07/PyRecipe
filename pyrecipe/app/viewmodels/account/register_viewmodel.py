from pyrecipe.app.viewmodels.shared import ViewModelBase


class RegisterViewModel(ViewModelBase):
    """Viewmodel used for the /account/register view."""

    def __init__(self):
        super().__init__()
        self.name = self.request_dict.name
        self.email = self.request_dict.email.lower().strip()
        self.password = self.request_dict.password.strip()

    def validate(self) -> None:
        if not self.name or not self.name.strip():
            self.error = "You must specify a name."
        elif not self.email or not self.email.strip():
            self.error = "You must specify an email address."
        elif not self.password:
            self.error = "You must specify a password."
        elif len(self.password) < 5:
            self.error = "The password must be at least 5 characters."
