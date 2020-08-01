"""Fixtures for the pyrecipe/app/views module."""

import pytest

from pyrecipe.app import app as flask_app


class User:
    def __init__(self, email, password, name="dude"):
        self.name, self.email, self.password = name, email, password
        self.id = "12345"

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    client = flask_app.test_client()

    # noinspection PyBroadException,PyUnusedLocal
    try:
        pyrecipe.app.register_blueprints()
    except Exception as x:
        # print(x)
        pass

    yield client
