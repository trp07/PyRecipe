# Testing Database
## mongodb
- The [mongodb/](https://github.com/trp07/PyRecipe/tree/master/tests/testing_db/mongodb) directory contains **user** and **recipe** collections for testing.
- Use the [mongorestore cli](https://docs.mongodb.com/manual/reference/program/mongorestore/#examples) that comes with installing m mongodb to load the database information.

### Test DB Entries
- The test database will include three **users**, each with three distinct **recipes**.
- Users:
  - King Arthur, email: **kingarthur@mail.com**
  - Brian, email: **brian@mail.com**
  - Black Knight, email: **blackknight@mail.com**
- To login a user, use the **cookbook.User.login_user** class method.
- Once a user instance is returned, then manipulation of user data and recipes can begin.

### Example
```python
from pyrecipe.storage import mongo_setup
from pyrecipe.cookbook import User
from pyrecipe.cookbook import Recipe

mongo_setup.global_init(db_name="pyrecipe_tester")

user = User.login_user(email="kingarthur@mail.com")
recipes = [Recipe(recipe) for recipe in user.recipes]

# continue testing/working
```
  
