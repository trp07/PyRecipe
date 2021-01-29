"""Tests for the pyrecipes/services/images/image_importer.py module."""

import hashlib
import pathlib
from unittest.mock import Mock

import pytest

from pyrecipe.services.images import image_importer as imp


def test_process_image(pillowmocks, imgfile, mocker):
    """
    GIVEN an image file via the recipe usecase
    WHEN process_image is called
    THEN assert the correct sequence occurs and the new filename is returned
    """
    pillowmocks = pillowmocks
    imgimport_mock = mocker.patch.object(imp.ImageImporter, "process_image")
    imgimport_mock.return_value = "processed.jpg"
    result = imp.process_image(imgfile)
    assert result == "processed.jpg"


############ Internal Functions ##############################################

def test_ImageImporter_init(pillowmocks, imgfile):
    """
    GIVEN an image path
    WHEN creating an ImageImporter instance
    THEN assert it is created correctly
    """
    img = imp.ImageImporter(imgfile)
    assert img._image is not None
    assert img._path == imgfile
    assert img.filetype == "jpg"


def test_ImageImporter_process_image_fileAlreadyExists(pillowmocks, imgfile, mocker, monkeypatch):
    """
    GIVEN an ImageImporter instance
    WHEN calling process_image on an image that was already imported
    THEN assert no processing is done and the saved filename is returned
    """
    rename_mock =mocker.patch.object(imp.ImageImporter, "_rename_image")
    rename_mock.return_value = "hashed.jpg"
    check_mock = mocker.patch.object(imp.ImageImporter, "_check_if_image_already_exists")
    check_mock.return_value = True

    img = imp.ImageImporter(imgfile)
    monkeypatch.setattr(pathlib.Path, "is_file", lambda x: True)
    monkeypatch.setattr(pathlib.Path, "unlink", lambda x: None)

    result = img.process_image()
    assert result == "hashed.jpg"


def test_ImageImporter_process_image_fileDoesNotExists(pillowmocks, imgfile, mocker, monkeypatch):
    """
    GIVEN an ImageImporter instance
    WHEN calling process_image on a new image
    THEN assert processing is done and the saved filename is returned
    """
    rename_mock =mocker.patch.object(imp.ImageImporter, "_rename_image")
    rename_mock.return_value = "hashed.jpg"
    check_mock = mocker.patch.object(imp.ImageImporter, "_check_if_image_already_exists")
    check_mock.return_value = False
    resize_mock = mocker.patch.object(imp.ImageImporter, "_resize_image")

    img = imp.ImageImporter(imgfile)
    monkeypatch.setattr(pathlib.Path, "is_file", lambda x: True)
    monkeypatch.setattr(pathlib.Path, "unlink", lambda x: None)

    result = img.process_image()
    assert result == "hashed.jpg"


def test_ImageImporter_process_image_NotAValidFile(pillowmocks, imgfile, mocker, monkeypatch):
    """
    GIVEN an ImageImporter instance
    WHEN calling process_image on a new image
    THEN assert processing is done and the saved filename is returned
    """
    rename_mock =mocker.patch.object(imp.ImageImporter, "_rename_image")
    rename_mock.return_value = "hashed.jpg"
    check_mock = mocker.patch.object(imp.ImageImporter, "_check_if_image_already_exists")
    check_mock.return_value = False
    resize_mock = mocker.patch.object(imp.ImageImporter, "_resize_image")

    img = imp.ImageImporter(imgfile)
    monkeypatch.setattr(pathlib.Path, "is_file", lambda x: False)
    monkeypatch.setattr(pathlib.Path, "unlink", lambda x: None)

    result = img.process_image()
    assert result == None


def test_ImageImporter_rename_image(pillowmocks, imgfile, mocker):
    """
    GIVEN an ImageImporter instance
    WHEN calling _rename_image
    THEN assert the correct name is returned
    """
    hash_mock = mocker.patch.object(hashlib, "md5")
    hash_mock.return_value.hexdigest.return_value = "hashed"

    img = imp.ImageImporter(imgfile)
    result = img._rename_image()
    assert result == "hashed.jpg"


@pytest.mark.parametrize("test_input", [3, 6, 8])
def test_ImageImporter_resize_image(test_input, pillowmocks, imgfile):
    img_mock, exf_mock = pillowmocks
    exf_mock.__getitem__.side_effect = "Orientation"
    exf_mock.keys.return_value = ["Orientation"]
    img_mock.getexif.return_value = {"Orientation": test_input}

    img = imp.ImageImporter(imgfile)
    img._image = img_mock
    img._resize_image()


@pytest.mark.parametrize("test_input, expected", [(True, True), (False, False)])
def test_ImageImporter_check_if_image_already_exists(test_input, expected, pillowmocks, imgfile, mocker):
    """
    GIVEN an image to import
    WHEN _check_if_image_already_exists is called
    THEN return True or False if the file already exists
    """
    path_mock = mocker.patch.object(pathlib, "Path")
    path_mock.return_value.is_file.return_value = test_input

    img = imp.ImageImporter(imgfile)
    result = img._check_if_image_already_exists("filename")
    assert result == expected

