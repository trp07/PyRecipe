"""
Tests for the pyrecipe.tradingpost.export_doc.py module.
fixtures defined in conftest.py
"""

import datetime
import pathlib

import pytest

import pyrecipe.services.export.export_doc
from pyrecipe.services.export.export_doc import FileWriter
from pyrecipe.services.export.export_doc import export_to_pdf
from pyrecipe.services.export.export_doc import SimpleDocTemplate, getSampleStyleSheet


def test_fw_init_mocked(mocker):
    """
    GIVEN a need for a FileWriter instance
    WHEN instantiated
    THEN assert properly created
    * mock out the pathlib functions to not create a directory
    """
    path_mock = mocker.patch.object(pathlib, "Path")
    path_mock.return_value.absolute.return_value.parent.return_value.joinpath.return_value.exists.return_value = (
        None
    )

    fw = FileWriter()
    assert isinstance(fw.doc, SimpleDocTemplate)
    assert isinstance(fw.styles, getSampleStyleSheet().__class__)


def test_fw_init():
    """
    GIVEN a need for a FileWriter instance
    WHEN instantiated
    THEN assert properly created
    """
    fw = FileWriter("PyRecipe")
    assert "PyRecipe" in fw.filename
    assert isinstance(fw.doc, SimpleDocTemplate)
    assert isinstance(fw.styles, getSampleStyleSheet().__class__)


def test_fw_create_doc(get_recipe, tmpdir):
    """
    GIVEN a db with users and recipes
    WHEN a user's selected recipes are selected for export
    THEN assert FileWriter writes a pdf file
    """
    recipes = get_recipe

    testdir = pathlib.Path(tmpdir).absolute()
    testfile = testdir.joinpath("pyrecipe_test1.pdf")

    fw = FileWriter(filename=str(testfile))

    result = fw.create_doc(recipes[0])
    assert result == 1
    assert pathlib.Path(testfile).absolute().exists()


def test_export_to_pdf(get_recipe, tmpdir):
    """
    GIVEN a call to export_to_pdf
    WHEN supplied with the correct params
    THEN assert the file is written and the correct return values returned
    """
    recipes = get_recipe

    testdir = pathlib.Path(tmpdir).absolute()
    testfile = testdir.joinpath("pyrecipe_test1.pdf")

    result = export_to_pdf(recipes[0], filename=str(testfile))
    assert result == str(testfile)
