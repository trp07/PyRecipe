# Storage Module
## Classes
Each class uses **mongoengine** to map to a MongoDB collection.
- **User**: holds all data for specific system users.
    - Required params: **name**, **email address**
    - Optional/Default params: **auth** (not implemented), **view**, **page_size**, **email_distros**
- **Recipe**: holds all data for specific recipes, owned by a user or shared amongst users.
    - Required params: **name**, **ingredients**, **num_igredients**, **directions**
    - Optional/Default params: **prep_time**, **cook_time**, **servings**, **tags**, **pictures**, **notes**, **ratings**, **favorite**, **deleted**
    - Embedded documents: **Ingredient**
- **Ingredient**: holds data for ingredients, embedded inside the **recipe** collection.
    - Required params: **name**, **quantity**
    - Optional/Default params: **unit**, **preparation**
    
## Usage
- The database must be initialized so the ODM classes can perform standard database operations.
- The following REPL session will show a few features by example.

```python
>>> from pyrecipe.storage import mongo_setup, User, Recipe, Ingredient

>>> mongo_setup.global_init(db_name="pyrecipe_tester")  # set db_name="pyrecipe" for actual use
                                                        # "pyrecipe_tester" db found in sourcecode
                                                        # "tests/testing_db/mongodb/" directory
# create a user                                                        
>>> u = User()
>>> u.name = 'Roger the Shrubber'
>>> u.email = 'roger@mail.com'
>>> u.save()
>>> u.id
'5c3ccd2f8e58582cfbf1cc35'

# create an ingredient
>>> i = Ingredient()
>>> i.name = 'spam'
>>> i.quantity = '12'
>>> i.unit = 'slices'
# don't use i.save(), just add it to the recipe

# create a recipe, and add all ingredients created
>>> r = Recipe()
>>> r.name = 'fried spam'
>>> r.ingredients.append(i)
>>> r.num_ingredients = 1
>>> r.directions = ['Heat skillet on medium heat.', 'Fry spam until brown.', 'Serve warm.']
>>> r.servings = 6
>>> r.tags = ['spam', 'breakfast', 'meat', 'protein', 'yuck']
>>> r.save()

# add the recipe to the user
>>> u.recipe_ids.append(r)
>>> u.save()
```
