"""
Tests for the pyrecipe.storage.mongo_setup.py modules, as well
as any other db setup module.
"""

import pytest
import mongoengine


from pyrecipe.storage import mongo_setup


def test_global_init_mongo(mocker):
    """
    GIVEN a mongoDB collection
    WHEN a connection is registered
    THEN asset correct function is called
    """
    reg_mock = mocker.patch.object(mongoengine, 'register_connection')

    mongo_setup.global_init()
    assert reg_mock.call_count == 1
