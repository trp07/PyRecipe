from typing import Optional

import flask
from flask import Request
from flask import current_app

from pyrecipe.app.helpers import request_dict
from pyrecipe.security import cookie_auth
from pyrecipe.usecases.account_uc import AccountUC


class ViewModelBase:
    """
    Base class for viewmodel subclasses to inherit from.

    Upon instantiation, subclasses will have access to the
    flask.request global variable, the request_dict will form
    the data structure containing all user-related content, and
    the user will be gained from any cookies contained in the
    request.
    """

    def __init__(self):
        self.request: Request = flask.request
        self.request_dict = request_dict.create(default_val="")
        self.error: Optional[str] = None
        self.user_id: Optional[int] = cookie_auth.get_user_id_via_auth_cookie(
            self.request, current_app.config["COOKIE_NAME"], current_app.config["SECRET_KEY"]
        )
        self.user = AccountUC(current_app.config["DB_DRIVER"]).find_user_by_id(self.user_id)

    def to_dict(self) -> dict:
        return self.__dict__
