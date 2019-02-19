"""
Test for the main.py module, the module that initializes the app.
"""

import pytest

from pyrecipe import main
from pyrecipe.app import app
from pyrecipe.storage import mongo_setup

def test_main(mocker):
    """
    GIVEN the pyrecipe application
    WHEN main.main() is called
    THEN assert the application is started
    """
    mongo_mock = mocker.patch.object(mongo_setup, "global_init")
    app_mock = mocker.patch.object(app, "run")
    main.main()

    assert mongo_mock.call_count == 1
    assert app_mock.call_count == 1


