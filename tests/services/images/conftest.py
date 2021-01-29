"""Configure/fixtures for testing the pyrecipe/services/images modules."""

import pathlib

import pytest

from pyrecipe.services.images import image_importer as imp


@pytest.fixture(scope="function")
def pillowmocks(mocker):
    """Mocks out the Pillow Image and ExifTags objects."""
    image_mock = mocker.patch.object(imp.Image, "open")
    exif_mock = mocker.patch.object(imp.ExifTags, "TAGS")
    yield (image_mock, exif_mock)


@pytest.fixture(scope="module")
def imgfile(tmpdir_factory):
    """Create a temporary directory for fake image files."""
    img_file = tmpdir_factory.mktemp("images").join("testimg.jpg")
    with open(img_file, "w") as fp:
        fp.write("test")

    return pathlib.Path(img_file)


@pytest.fixture(scope="function")
def pillowclasses(pillowmocks):
    """Mocks out PIL classes and returns stub classes."""
    return (MockPILImage(), MockExif())


class MockPILImage:
    def __init__(self):
        pass

class MockExif:
    def __init__(self):
        pass
