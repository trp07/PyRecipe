"""
Tests for the pyrecipe.tradingpost.import_doc.py module.

Fixtures found in conftest.py
1. recipe_setup
2. get_ingredients
"""

import pathlib
import time

import pikepdf

import pyrecipe.tradingpost.import_doc
from pyrecipe.tradingpost.import_doc import import_from_pdf
from pyrecipe.tradingpost.import_doc import _import_recipe
from pyrecipe.storage import Recipe



TESTDIR = pathlib.Path(__file__).absolute().parent
TESTFILE = TESTDIR.joinpath("testing_data/files/recipe_doc.pdf")


def test_file_exists():
    """First assert the test file exists."""
    assert TESTFILE.exists()


def test_import_from_pdf(mocker):
    """
    GIVEN a pyrecipe pdf file to import
    WHEN import_from_pdf is called with verbose=True
    THEN assert correct sequence is called and return value is
        properly constructed
    """
    data = {
        "dc:pyrecipe_version": "0.0.0",
        "dc:num_recipes": "3",
    }

    pike_mock = mocker.patch.object(pikepdf, "open")
    pike_mock.return_value.open_metadata.return_value = data

    imp_rec_mock = mocker.patch.object(pyrecipe.tradingpost.import_doc, "_import_recipe")
    imp_rec_mock.return_value = 123

    result = import_from_pdf("/fake/file/path.pdf", verbose=False)
    assert result == ["123", "123", "123"]
    assert imp_rec_mock.call_count == 3


def test_import_from_pdf_verbose(mocker, capsys):
    """
    GIVEN a pyrecipe pdf file to import
    WHEN import_from_pdf is called with verbose=True
    THEN assert correct sequence is called and return value is
        properly constructed and correct output printed
    """
    data = {
        "dc:pyrecipe_version": "0.0.0",
        "dc:num_recipes": "3",
    }

    pike_mock = mocker.patch.object(pikepdf, "open")
    pike_mock.return_value.open_metadata.return_value = data

    imp_rec_mock = mocker.patch.object(pyrecipe.tradingpost.import_doc, "_import_recipe")
    imp_rec_mock.return_value = 123

    result = import_from_pdf("/fake/file/path.pdf", verbose=True)
    out, err = capsys.readouterr()

    assert "Recipes embedded in file metadata: 3" in out
    assert result == ["123", "123", "123"]
    assert imp_rec_mock.call_count == 3


def test_import_recipes_verbose(recipe_setup, get_ingredients, mocker, capsys):
    """
    GIVEN a recipe in a pdf metadata
    WHEN import_recipe is called with verbose=True
    THEN assert the assert the correct sequence is called, the correct output
        prints, and the functions returns the correct value
    """
    recipe = recipe_setup
    recipe.name = 'test'
    recipe.ingredients = [get_ingredients]
    recipe.num_ingredients = 1
    recipe.directions = ['do a test!']
    recipe.save()

    rec_mock = mocker.patch.object(pyrecipe.tradingpost.import_doc, "Recipe")
    rec_mock.return_value = recipe

    metadata = pikepdf.open(TESTFILE).open_metadata()
    result = _import_recipe(metadata, 1, verbose=True)
    out, err = capsys.readouterr()

    assert result == recipe.id
    assert "+ Adding Recipe 1: hearty spam breakfast skillet" in out
    assert "<i: spam classic>" in out
    assert "<i: bell pepper>" in out
    assert "<i: onion>" in out
    assert "<i: dried basil>" in out
    assert "<i: potatoes>" in out
    assert "<i: eggs>" in out
    assert "<i: hot pepper sauce>" in out
    assert "<i: pepper>" in out
    assert "<i: salt>" in out
    assert "<i: cheddar cheese>" in out
    assert "<i: vegetable oil>" in out
