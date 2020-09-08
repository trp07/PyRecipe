## Outdated... will be updated shortly

## TradingPost Module
This module is designed to allow exporting and importing of user recipes.

## Functions
- **export_to_pdf**: Export a given list of user recipes to a pdf document.
    - **returns**: tuple(number of recipes exported, number of recipes written to metadata, file path of pdf document)
- **import_from_pdf**: Import a set of recipes from a pdf document to a user's account.
    - **returns**: List['Recipe.id'] a list of all the recipe id's that were imported

## Usage
- The database must be initialized so the classes can perform standard database operations.
- The following REPL session will show a few features by example.

```python
>>> from pyrecipe.storage import mongo_setup
>>> from pyrecipe.cookbook import User, Recipe
>>> from pyrecipe.tradingpost import export_to_pdf
>>> from pyrecipe.tradingpost import import_from_pdf

>>> mongo_setup.global_init(db_name="pyrecipe_tester")  # set db_name="pyrecipe" for actual use
                                                        # "pyrecipe_tester" db found in sourcecode
                                                        # "tests/testing_data/mongodb/" directory

>>> user = User.login_user(email='blackknight@mail.com')
>>> recipes = recipes = [Recipe(recipe) for recipe in user.recipes]

>>> export_to_pdf(recipes[0:2])
(2, 2, '/file/path/of/exported/file.pdf')


# now import the recipes at a later date...
>>> import_from_pdf('/file/path/of/exported/file.pdf')
["5c3ccd2f8e58582cfbf1cc32", "5c3ccd2f8e58582cfbf1cc33"]
```
