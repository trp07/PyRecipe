"""Module to set up the MongoDB connection."""

import mongoengine


def global_init():
    """Create/Register connection with mongodb.  DB name will be 'pyrecipe'."""
    mongoengine.register_connection(alias="core", name="pyrecipe")
