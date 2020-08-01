"""Fixtures for the pyrecipe/app/views module."""

import sys
import os

import pytest

from pyrecipe.app import app as flask_app


class TestUser:
    def __init__(self, email, password, name):
        self.name, self.email, self.password = name, email, password
        self.id = "12345"


@pytest.fixture(scope="function")
def testuser():
    """Returns a dummy test user for testing."""
    def _user(email, password, name="dude"):
        return TestUser(email, password, name)
    yield _user


@pytest.fixture(scope="function")
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
