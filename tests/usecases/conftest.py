"""Fixtures for use case testing."""

import pytest


######## RecipeUC fixtures ########


class Ingredient:
    def __init__(self, name):
        self.name = name


class Recipe:
    def __init__(self, _id, name, ingredients, tags, deleted, images):
        self.id = _id
        self.name = name
        self.ingredients = ingredients
        self.tags = [tag.lower() for tag in tags]
        self.deleted = deleted
        self.images = images


class RecipeDriver:
    def __init__(self, recipes):
        self.recipes = recipes

    def recipes_active(self):
        return [r for r in self.recipes if r.deleted == False]

    def recipes_deleted(self):
        return [r for r in self.recipes if r.deleted == True]

    def recipes_all(self):
        return self.recipes

    def recipe_find_by_id(self, _id):
        for r in self.recipes:
            if str(r.id) == str(_id):
                return r

    def recipe_create(
        self, name, prep_time, cook_time, servings, ingredients, directions, tags, notes, images,
    ):
        r = Recipe(
            _id=789, name=name, ingredients=ingredients, tags=tags, deleted=False, images=images,
        )
        return r

    def recipe_edit(
        self, _id, name, prep_time, cook_time, servings, ingredients, directions, tags, notes,
    ):
        r = self.recipe_find_by_id(_id)
        r.name = name
        r.prep_time = prep_time
        r.cook_time = cook_time
        r.servings = servings
        r.ingredients = ingredients
        r.directions = directions
        r.notes = notes
        r.tags = tags
        return r

    def recipes_find_by_tag(self, tags):
        tags = [tag.lower() for tag in tags]
        rec = []
        for r in self.recipes:
            if set(tags).issubset(set(r.tags)):
                rec.append(r)
        return rec

    def recipes_get_tags(self):
        t = set()
        for r in self.recipes:
            t.update(set(r.tags))
        return list(t)

    def recipe_delete(self, recipe_id):
        r = self.recipe_find_by_id(recipe_id)
        if r:
            r.deleted = True
            return 1
        else:
            return 0


@pytest.fixture(scope="function")
def rec_driver():
    r1 = Recipe(
        _id=123,
        name="recipe1",
        ingredients=Ingredient("garlic"),
        tags=["quick", "spicy"],
        deleted=False,
        images = ["testimg.jpg"],
    )
    r2 = Recipe(
        _id=456,
        name="recipe2",
        ingredients=Ingredient("onion"),
        tags=["slow", "spicy"],
        deleted=True,
        images = [],
    )

    d = RecipeDriver([r1, r2])
    yield d


######## AccountUC fixtures ########


class User:
    def __init__(self, _id, name, email, password):
        self.id = _id
        self.name = name
        self.email = email
        self.password = password


class UserDriver:
    def __init__(self, users):
        self.users = users

    def user_login(self, email, password):
        for u in self.users:
            if email == u.email:
                if password == u.password:
                    return u

    def user_create(self, name, email, password):
        for u in self.users:
            if email == u.email:
                return None
        return User(789, name, email, password)

    def user_find_by_id(self, _id):
        for u in self.users:
            if str(_id) == str(u.id):
                return u


@pytest.fixture(scope="function")
def act_driver():
    u1 = User(_id=123, name="alice", email="alice@mail.com", password="alicerulz")

    u2 = User(_id=456, name="bob", email="bob@mail.com", password="bobrulz")

    d = UserDriver([u1, u2])
    yield d
