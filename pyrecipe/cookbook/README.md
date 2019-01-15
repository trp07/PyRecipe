# Cookbook Module
## Classes
Each class has an associated **interface** that must be implemented in order to have an expected level of behavior.
- **User**: a class that abstracts the database interaction and provides an interface to the MongoDB **user collection**.
- **Recipe**: a class that abstracts the database interaction and provides an interface to the MongoDB **recipe collection**.

## Usage
- The database must be initialized so the classes can perform standard database operations.
- The following REPL session will show a few features by example.
```python
>>> from pyrecipe.storage import mongo_setup
>>> from pyrecipe.cookbook import User, Recipe

>>> mongo_setup.global_init(db_name="pyrecipe_tester")  # set db_name="pyrecipe" for actual use
                                                        # "pyrecipe_tester" db found in sourcecode 
                                                        # "tests/testing_db/mongodb/" directory                                               

>>> user = User.login_user(email="blackknight@mail.com")
>>> user.name
'Black Knight'

>>> recipes = [Recipe(recipe) for recipe in user.recipes]
>>> recipes[0].name
'hearty spam breakfast skillet'

>>> new_user = User.create_user(name="Roger the Shrubber", email="roger@mail.com")
>>> new_user._id
"5c3ccd2f8e58582cfbf1cc35"

>>> len(new_user.recipes)
0

>>> new_recipe = Recipe.create_recipe(
                      name='fried spam', 
                      ingredients={'name':'spam', 'quantity':'1', 'unit':'slice'},
                      directions=['Heat skillet on medium heat.', 'Fry spam until brown.', 'Serve warm.'],
                  )

>>> new_user.add_recipe(new_recipe)
>>> len(new_user.recipes)
1
```
