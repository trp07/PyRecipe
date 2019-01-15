"""Tests for the pyrecipe.tradingpost.filewriter.py module."""

import datetime
import pathlib

import mongoengine
import pytest

from pyrecipe.tradingpost.filewriter import FileWriter
from pyrecipe.tradingpost.filewriter import export_to_pdf
from pyrecipe.tradingpost.filewriter import SimpleDocTemplate, getSampleStyleSheet
from pyrecipe.cookbook import User, Recipe


def test_fw_init():
    """
    GIVEN a need for a FileWriter instance
    WHEN instantiated
    THEN assert properly created
    """
    fw = FileWriter()
    assert "PyRecipe_" in fw.filename
    assert isinstance(fw.doc, SimpleDocTemplate)
    assert isinstance(fw.styles, getSampleStyleSheet().__class__)


def test_fw_create_doc(tmpdir):
    """
    GIVEN a db with users and recipes
    WHEN a user's selected recipes are selected for export
    THEN assert FileWriter writes a pdf file
    """
    db = mongoengine.connect(db='pyrecipe_tester', alias='core', host='mongodb://localhost')

    user = User.login_user(email="blackknight@mail.com")
    recipes = [Recipe(r) for r in user.recipes]
    db.close()

    testdir = pathlib.Path(tmpdir).absolute()
    testfile = testdir.joinpath('pyrecipe_test1.pdf')

    fw = FileWriter(filename=str(testfile))

    result = fw.create_doc(recipes)
    assert result == 3
    assert pathlib.Path(testfile).absolute().exists()


def test_export_to_pdf(mocker):
    """
    GIVEN a call to export_to_pdf
    WHEN supplied with the correct params
    THEN assert FileWriter.create_doc() is called with no errors
    """
    recipes = ['r1', 'r2']
    create_mock = mocker.patch.object(FileWriter, 'create_doc')

    export_to_pdf(recipes)
    assert create_mock.call_count == 1

