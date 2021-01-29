"""A config module for the app."""

import os
import uuid

from pyrecipe.static import IMAGEDIR
from pyrecipe.storage.mongo import MongoDriver



class ProdConfig:
    """A class to store configuration data for Production Deployment."""

    APP_NAME = "PyRecipe"
    SECRET_KEY = os.environ.get("SECRET_KEY") or str(uuid.uuid4()).replace("-", "")
    DB_URI = os.environ.get("MONGODB_URI") or "pyrecipe_prod"
    DB_DRIVER = MongoDriver
    DEBUG = False
    TESTING = False
    COOKIE_NAME = "pyrecipe_prod"
    ALLOWED_IMAGES = ["jpg", "jpeg", "png", "gif"]
    IMAGEDIR = IMAGEDIR


class DevConfig:
    """A class to store configuration data for Development Deployment."""

    APP_NAME = "PyRecipe"
    SECRET_KEY = "SecretDevKey"
    DB_URI = os.environ.get("MONGODB_URI") or "pyrecipe_tester"
    DB_DRIVER = MongoDriver
    DEBUG = True
    TESTING = True
    COOKIE_NAME = "pyrecipe_dev"
    ALLOWED_IMAGES = ["jpg", "jpeg", "png", "gif"]
    IMAGEDIR = IMAGEDIR
