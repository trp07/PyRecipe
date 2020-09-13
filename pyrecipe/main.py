"""The main entry point for the application."""

from pyrecipe import __version__ as VERSION
from pyrecipe.app import app

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
""".format(
    VERSION
)


def main():
    """Run the app."""
    print(BANNER, flush=True)
    app.config.get("DB_DRIVER").db_initialize(db_name=app.config.get("DB_URI"), verbose=True)
    app.run()


if __name__ == "__main__":
    main()
