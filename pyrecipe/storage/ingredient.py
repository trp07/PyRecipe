"""
ODM for MongoDB

* Ingredient -- DB representation of Recipe instance.
"""

import mongoengine


class Ingredient(mongoengine.EmbeddedDocument):
    """
    ODM Class that maps to the Recipes embedded collection in MongoDB.
    This class is embedded inside the Recipe class.

    REQUIRED params:
    :param name: (str) the name of the ingredient.
    :param quantity: (str) the amount of the ingredient.

    NOT-REQUIRED param:
    :param unit: (str) the unit of measurement.
    """

    name = mongoengine.StringField(required=True)
    quantity = mongoengine.StringField(required=True)
    unit = mongoengine.StringField(required=False)

    meta = {"db_alias": "core", "collection": "ingredients"}
