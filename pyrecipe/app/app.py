"""
The main Flask app controller.  This will register
all the views as blueprints in the views/ directory.
"""

import pathlib

import flask
import secure

from pyrecipe.frontend import TEMPLATESDIR
from pyrecipe.static import STATICDIR
from pyrecipe.app.views import home_views
from pyrecipe.app.views import account_views
from pyrecipe.app.views import recipe_views
from pyrecipe.app.views import rest_views


####### Create the app instance ##############################################

rootpath = str(pathlib.Path(__file__).absolute().parents[1])

app = flask.Flask(
    __name__,
    template_folder=str(TEMPLATESDIR),
    static_folder=str(STATICDIR),
    root_path=rootpath,
)


####### Register app blueprints ##############################################

def register_blueprints(app) -> None:
    app.register_blueprint(home_views.blueprint)
    app.register_blueprint(account_views.blueprint)
    app.register_blueprint(recipe_views.blueprint)
    app.register_blueprint(rest_views.blueprint)


register_blueprints(app)


####### Add secure headers ###################################################

secure_headers = secure.SecureHeaders()

@app.after_request
def set_secure_headers(response):
    secure_headers.flask(response)
    return response
