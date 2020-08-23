"""
The main Flask app controller.  This will register
all the views as blueprints in the views/ directory.
"""

import flask
import secure

from pyrecipe.frontend import TEMPLATESDIR
from pyrecipe.static import STATICDIR
from pyrecipe.app.views import home_views
from pyrecipe.app.views import account_views
from pyrecipe.app.views import recipe_views
import pyrecipe.config as config


app = flask.Flask(
    __name__, template_folder=str(TEMPLATESDIR), static_folder=str(STATICDIR)
)


####### Config app and register blueprints

app.config.from_object(config.DevConfig)

def register_blueprints() -> None:
    global app
    app.register_blueprint(home_views.blueprint)
    app.register_blueprint(account_views.blueprint)
    app.register_blueprint(recipe_views.blueprint)


register_blueprints()

####### Add secure headers
secure_headers = secure.SecureHeaders()

@app.after_request
def set_secure_headers(response):
    secure_headers.flask(response)
    return response
