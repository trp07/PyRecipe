## TradingPost Module
This module is designed to allow exporting and importing of user recipes.

## Functions
- **export_to_pdf**: Export a given list of user recipes to a pdf document.
- **import_from_pdf**: (NOT YET IMPLEMENTED) Import a set of recipes from a pdf document to a user's account.

## Usage
- The database must be initialized so the classes can perform standard database operations.
- The following REPL session will show a few features by example.

```python
>>> from pyrecipe.storage import mongo_setup
>>> from pyrecipe.cookbook import User, Recipe
>>> from pyrecipe.tradingpost import export_to_pdf

>>> mongo_setup.global_init(db_name="pyrecipe_tester")  # set db_name="pyrecipe" for actual use
                                                        # "pyrecipe_tester" db found in sourcecode 
                                                        # "tests/testing_db/mongodb/" directory 

>>> user = User.login_user(email='blackknight@mail.com')
>>> recipes = recipes = [Recipe(recipe) for recipe in user.recipes]

>>> export_to_pdf(recipes[0:2])
# file written: PyRecipe_YYY-MM-DD_HH:MM.pdf
```
