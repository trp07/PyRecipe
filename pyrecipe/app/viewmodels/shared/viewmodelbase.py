from typing import Optional

import flask
from flask import Request

from pyrecipe.app.helpers import request_dict
from pyrecipe.app.helpers import cookie_auth


class ViewModelBase:
    def __init__(self):
        self.request: Request = flask.request
        self.request_dict = request_dict.create(default_val="")

        self.error: Optional[str] = None
        self.user_id: Optional[int] = cookie_auth.get_user_id_via_auth_cookie(self.request)

    def to_dict(self):
        return self.__dict__
