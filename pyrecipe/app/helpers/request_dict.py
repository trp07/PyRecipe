import flask


class RequestDictionary(dict):
    """
    Dict subclass that enables one to retrieve key, value
    pairs via class.attr method.
    """

    def __init__(self, *args, default_val=None, **kwargs):
        self.default_val = default_val
        super().__init__(*args, **kwargs)

    def __getattr__(self, key):
        """
        So you can access key by attribute...

        i.e.
        r.name -> r["name"]
        """
        return self.get(key, self.default_val)


def create(default_val=None, **route_args) -> RequestDictionary:
    """
    Creates and returns an instance of RequestDictionary.

    The dict "data" unpacks the kwargs gained in order from
    "least important" to "most important".  First it unpacks
    the URL query string, then headers, and then the form data
    from the flask.request global.  Then, additional args from
    the routing functions/methods themselves, if passed to the
    function.
    """
    request = flask.request

    data = {**request.args, **request.headers, **request.form, **route_args}

    return RequestDictionary(data, default_val=default_val)
