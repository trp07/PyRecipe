"""Tests for pyrecipe/app/views."""

import pytest

from flask import Response

from pyrecipe.app import app as flask_app
from pyrecipe.app.views import rest_views


def test_index():
    """
    GIVEN a running app
    WHEN /rest is requested
    THEN assert no errors and the proper dict response is returned
    """
    with flask_app.test_request_context(path="/rest", data=None):
        resp: Response = rest_views.index()
    assert resp == {"alive": True}
