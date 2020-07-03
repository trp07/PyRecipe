import pytest

from pyrecipe.storage.shared import ImageModel

####### globals #########

IMAGE = {
    "recipe_id": "abcdefg",
    "filepath": "/file/path",
    "description": "picture of food",
}


###### test funcs #########

def test_imagemodel_init():
    """Verifies a ImageModel is properly instantiated."""
    image = ImageModel(**IMAGE)
    assert image.recipe_id == "abcdefg"
    assert image.filepath == "/file/path"
    assert image.description == "picture of food"


def test_imagemodel_fromdict():
    """Verifies a ImageModel is properly instantiated via the
    from_dict() method."""
    image = ImageModel.from_dict(IMAGE)
    assert image.recipe_id == "abcdefg"
    assert image.filepath == "/file/path"
    assert image.description == "picture of food"


def test_imageModel_todict():
    """Verifies a properly formed dict is returned from the
    ImageModel.to_dict() method."""
    image = ImageModel(**IMAGE)
    image_dict = image.to_dict()
    assert image_dict == IMAGE
