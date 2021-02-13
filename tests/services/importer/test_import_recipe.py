"""Tests for the pyrecipe/services/importer/import_recipe.py module."""

import pytest

import pyrecipe.services.importer.import_recipe as imp


class MockedHTTPResponse:
    def __init__(self): pass
    def title(self): return "test_name"
    def total_time(self): return "10"
    def yields(self): return "5"
    def ingredients(self): return ["a", "b"]
    def instructions(self): return "1\n2"
    def host(self): return "tester.com"
    def nutrients(self): return {"carb": "10", "protein": "10"}
    def image(self): return "url-to-image"


def test_import_from_url(mocker):
    """
    GIVEN a url to a recipe
    WHEN asked to import it
    THEN assert the proper elements are returned
    """
    scrape_mock = mocker.patch.object(imp, "scrape_me")
    scrape_mock.return_value = MockedHTTPResponse()

    result = imp.import_from_url("testurl")
    assert result["name"] == "test_name"
    assert result["prep_time"] == 1
    assert result["cook_time"] == "10"
    assert result["servings"] == "5"
    assert result["ingredients"] == ["a", "b"]
    assert result["directions"] == ["1", "2"]
    assert result["tags"] == ["imported", "tester"]
    assert result["notes"] == ["Imported from: testurl", "carb: 10", "protein: 10"]


def test_import_from_url_websiteError(mocker):
    """
    GIVEN a url to a recipe
    WHEN asked to import it but the first attempt returns a WebsiteNotImplementedError
    THEN assert the proper elements are returned after the second attempt
    """
    scrape_mock = mocker.patch.object(imp, "scrape_me")
    scrape_mock.side_effect = [imp.WebsiteNotImplementedError("testurl") ,MockedHTTPResponse()]

    result = imp.import_from_url("testurl")
    assert result["name"] == "test_name"
    assert result["prep_time"] == 1
    assert result["cook_time"] == "10"
    assert result["servings"] == "5"
    assert result["ingredients"] == ["a", "b"]
    assert result["directions"] == ["1", "2"]
    assert result["tags"] == ["imported", "tester"]
    assert result["notes"] == ["Imported from: testurl", "carb: 10", "protein: 10"]


def test_import_from_url_exception(mocker):
    """
    GIVEN a url to a recipe
    WHEN asked to import it but the first attempt returns a WebsiteNotImplementedError
    THEN assert the proper elements are returned after the second attempt
    """
    scrape_mock = mocker.patch.object(imp, "scrape_me")
    scrape_mock.side_effect = Exception()

    result = imp.import_from_url("testurl")
    assert "error" in result.keys()
