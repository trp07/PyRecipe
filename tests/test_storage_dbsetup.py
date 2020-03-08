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
    WHEN a connection is registered with verbose=False (default)
    THEN asset correct function is called
    """
    reg_mock = mocker.patch.object(mongoengine, 'register_connection')

    mongo_setup.global_init()
    assert reg_mock.call_count == 1


def test_global_init_mongo_verbose(mocker, capsys):
    """
    GIVEN a mongoDB collection
    WHEN a connection is registered with verbose=True
    THEN asset correct function is called and output prints
    """
    reg_mock = mocker.patch.object(mongoengine, 'register_connection')

    mongo_setup.global_init(db_name='pyrecipe_tester', verbose=True)
    out, err = capsys.readouterr()
    assert '[+] MongoDB connection registered to database: pyrecipe_tester' in out
    assert reg_mock.call_count == 1
