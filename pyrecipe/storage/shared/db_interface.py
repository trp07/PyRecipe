"""
Recipe Database Interface.

Abstract interface all DB Drivers will inherit from to
ensure consistent use and enable Interface Segragation.
"""

from abc import ABCMeta
from abc import abstractmethod


class DBInitInt(metaclass=ABCMeta):
    """
    Interface to initialize the DB to ensure consistency among
    DB types.
    """

    @abstractmethod
    def db_initialize() -> None:
        """Do what's needed to initialize the DB."""
        pass
