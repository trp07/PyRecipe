"""
ODM for MongoDB

* Image -- DB representation of recipe images.
"""

import mongoengine


class Image(mongoengine.EmbeddedDocument):
    """
    ODM Class that maps to the Recipes embedded collection in MongoDB.
    This class is embedded inside the Recipe class.

    REQUIRED params:
    :param recipe_id: (str) the recipe id this image belongs to.
    :param filepath: (str) the filepath location of the image.
    :param description: (str) description of the image.
    """

    recipe_id = mongoengine.StringField(required=True)
    filepath = mongoengine.StringField(required=True)
    description = mongoengine.StringField(required=True)

    meta = {"db_alias": "core", "collection": "images"}
