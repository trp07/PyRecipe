"""A config module for Flask."""

import os
import uuid

class Config:
    """A class to store configuration data."""
    SECRET_KEY = os.environ.get("SECRET_KEY") or str(uuid.uuid4()).replace("-", "")
    MONGODB_URI = os.environ.get("MONGODB_URI") or "pyrecipe_tester"
