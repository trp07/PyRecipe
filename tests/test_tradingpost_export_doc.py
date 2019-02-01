"""
Tests for the pyrecipe.tradingpost.export_doc.py module.

"mongodb" is a fixture defined in conftest.py
"""

import datetime
import pathlib

import pytest

import pyrecipe.tradingpost.export_doc
from pyrecipe.tradingpost.export_doc import FileWriter
from pyrecipe.tradingpost.export_doc import export_to_pdf
from pyrecipe.tradingpost.export_doc import SimpleDocTemplate, getSampleStyleSheet
from pyrecipe.storage import User, Recipe


def test_fw_init_mocked(mocker):
    """
    GIVEN a need for a FileWriter instance
    WHEN instantiated
    THEN assert properly created
    * mock out the pathlib functions to not create a directory
    """
    path_mock = mocker.patch.object(pathlib, 'Path')
    path_mock.return_value.absolute.return_value.parent.return_value.joinpath.return_value.exists.return_value = None

    fw = FileWriter()
    assert isinstance(fw.doc, SimpleDocTemplate)
    assert isinstance(fw.styles, getSampleStyleSheet().__class__)


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


def test_fw_create_doc(mongodb, tmpdir):
    """
    GIVEN a db with users and recipes
    WHEN a user's selected recipes are selected for export
    THEN assert FileWriter writes a pdf file
    """
    db = mongodb

    user = User.login(email="blackknight@mail.com", password_hash="Not Implemented")
    recipes = user.recipe_ids

    testdir = pathlib.Path(tmpdir).absolute()
    testfile = testdir.joinpath('pyrecipe_test1.pdf')

    fw = FileWriter(filename=str(testfile))

    result = fw.create_doc(recipes)
    assert result == 3
    assert pathlib.Path(testfile).absolute().exists()


def test_export_to_pdf_mocked(mocker):
    """
    GIVEN a call to export_to_pdf
    WHEN supplied with the correct params
    THEN assert FileWriter.create_doc() and _write_metadata are called with no errors
    * mock out the calls to other functions
    """
    recipes = ['r1', 'r2']
    create_mock = mocker.patch.object(FileWriter, 'create_doc')
    meta_mock = mocker.patch.object(pyrecipe.tradingpost.export_doc, '_write_metadata')

    result = export_to_pdf(recipes, verbose=False)
    assert create_mock.call_count == 1
    assert meta_mock.call_count == 1


def test_export_to_pdf(mongodb, tmpdir):
    """
    GIVEN a call to export_to_pdf
    WHEN supplied with the correct params
    THEN assert the file is written and the correct return values returned
    """
    db = mongodb

    user = User.login(email="blackknight@mail.com", password_hash="Not Implemented")
    recipes = user.recipe_ids

    testdir = pathlib.Path(tmpdir).absolute()
    testfile = testdir.joinpath('pyrecipe_test1.pdf')

    result = export_to_pdf(recipes, filename=str(testfile), verbose=True)
    assert result == (3, 3, str(testfile))

