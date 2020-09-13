"""
Test for the main.py module, the module that initializes the app.
"""

import pytest

from pyrecipe import main
from pyrecipe.app import app


def test_main(mocker):
    """
    GIVEN the pyrecipe application
    WHEN main.main() is called
    THEN assert the application is started
    """
    app_cfg_mock = mocker.patch.object(app.config, "get")
    app_run_mock = mocker.patch.object(app, "run")
    main.main()

    assert app_cfg_mock.call_count == 2
    assert app_run_mock.call_count == 1


