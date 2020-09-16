"""REST interface for the app."""

import flask


blueprint = flask.Blueprint("rest", __name__)


@blueprint.route("/rest")
@blueprint.route("/rest/")
def index():
    """Just return whether the app is alive or not."""
    return {
        "alive": True,
    }
