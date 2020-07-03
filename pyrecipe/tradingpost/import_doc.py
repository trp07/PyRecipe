"""
PDF file reader for selected recipes to import.


Noteable Classes/Functions:
1.  _import_recipe - fucntion that iterates through the required fields
    in a storage.Recipe and storage.Ingredient class and assigns to those
    attributes.  Saves the recipe into the MongoDB collection and returns
    the recipe id.

Usage:
1.  import_from_pdf - The main interface for this module.  Uses the
    pikepdf third-party module to retrieve the PDF file metadata to read
    any recipes that are encoded there.  Returns a list of Recipe.id's for
    all recipes imported.
"""

#from typing import List
#
#import pikepdf
#
#from pyrecipe.storage import Recipe, Ingredient
#
#
#def _import_recipe(data: dict, index: int, verbose=False) -> "Recipe.id":
#    """
#    Adds the given data dictionary into the recipes DB collection.
#
#    :param data: (dict) the metadata dictionary where the recipes are stored.
#    :param index: (int) which # recipe to retrieve and add.
#    :param verbose: (bool) print verbose output.
#    :returns: (Recipe.id) the database ID of the recipe added.
#    """
#    r_base = "dc:r" + str(index) + "."
#    recipe = Recipe()
#
#    recipe.name = data[r_base + "name"]
#    recipe.num_ingredients = int(data[r_base + "num_ingredients"])
#    recipe.directions = data[r_base + "directions"]
#    recipe.prep_time = float(data[r_base + "prep_time"])
#    recipe.cook_time = float(data[r_base + "cook_time"])
#    recipe.servings = int(data[r_base + "servings"])
#    recipe.tags = data[r_base + "tags"]
#    recipe.notes = data[r_base + "notes"]
#
#    if verbose:
#        print("+ Adding Recipe {}: {}".format(index, recipe.name))
#
#    for i in range(1, recipe.num_ingredients + 1):
#        i_base = r_base + "i" + str(i) + "."
#
#        ingredient = Ingredient()
#        ingredient.name = data[i_base + "name"]
#        ingredient.quantity = data[i_base + "quantity"]
#        ingredient.unit = data[i_base + "unit"]
#        ingredient.preparation = data[i_base + "preparation"]
#
#        recipe.ingredients.append(ingredient)
#
#        if verbose:
#            print("    <i: {}>".format(ingredient.name))
#
#    recipe.save()
#    return recipe.id
#
#
#def import_from_pdf(filepath: str, verbose: bool = False) -> List["Recipe.id"]:
#    """
#    Function that will delegate to helper functions to import the recipes written
#    into the PDF file metadata and write into the local DB instance.
#
#    :param filepath: (str) filepath of the file to import.
#    :param verbose: (bool) print verbose output.
#    :returns: list[Recipe.id] a list of all the recipe id's added to the
#        database.
#    """
#    pdf = pikepdf.open(filepath)
#    meta = pdf.open_metadata()
#
#    version_num = meta["dc:pyrecipe_version"]
#    num_recipes = int(meta["dc:num_recipes"])
#
#    if verbose:
#        print("Recipes embedded in file metadata: {}".format(num_recipes))
#
#    result = []
#    for i in range(1, num_recipes + 1):
#        recipe_id = _import_recipe(meta, i, verbose)
#        result.append(str(recipe_id))
#
#    return result
