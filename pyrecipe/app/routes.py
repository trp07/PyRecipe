"""Routes for the Flask App."""

from pyrecipe.app import app
from pyrecipe.cookbook import User, Recipe

@app.route('/')
def index(method=['GET']):
    return """
        <h1>PyRecipe</h1>
        <p>A Cookbook Designed in Python.</p>
        <p>This Project is Under Development.  Please be Patient! :)</p>
        """


@app.route('/list')
def list_recipes(method=['GET']):
    user = User.login_user(email='blackknight@mail.com')
    recipes = [Recipe(recipe) for recipe in user.recipes]

    result = ''
    for recipe in recipes:
        result += "<li>{}</li>".format(recipe.name)

    return result
