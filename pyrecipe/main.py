"""The main entry point for the application."""

from pyrecipe import __version__ as VERSION
from pyrecipe.app import app
from pyrecipe.storage import mongo_setup

BANNER = r"""
  _____       _____           _
 |  __ \     |  __ \         (_)
 | |__) |   _| |__) |___  ___ _ _ __   ___
 |  ___/ | | |  _  // _ \/ __| | '_ \ / _ \
 | |   | |_| | | \ \  __/ (__| | |_) |  __/
 |_|    \__, |_|  \_\___|\___|_| .__/ \___|
         __/ |                 | |
        |___/                  |_|

version: {}

_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^
""".format(VERSION)


if __name__ == '__main__':

    print(BANNER, flush=True)

    mongo_setup.global_init(db_name=app.config.get("MONGODB_URI"), verbose=True)
    app.run()
