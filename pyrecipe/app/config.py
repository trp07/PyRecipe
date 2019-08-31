"""A config module for Flask."""

import os
import uuid

class ProdConfig:
    """A class to store configuration data for Production Deployment."""
    SECRET_KEY = os.environ.get("SECRET_KEY") or str(uuid.uuid4()).replace("-", "")
    MONGODB_URI = os.environ.get("MONGODB_URI") or "pyrecipe_tester"
    DEBUG = False

class DevConfig:
    """A class to store configuration data for Development Deployment."""
    SECRET_KEY = os.environ.get("SECRET_KEY") or str(uuid.uuid4()).replace("-", "")
    MONGODB_URI = os.environ.get("MONGODB_URI") or "pyrecipe_tester"
    DEBUG = True
