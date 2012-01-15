"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password

from decorator import decorator
import jsonpickle
from pylons import request
import warnings
from pylons import config
from routes import url_for
from pylons.decorators.util import get_pylons

def ourjsonify(func, *args, **kwargs):
    """Action decorator that formats output for JSON

    Given a function that will return content, this decorator will turn
    the result into JSON, with a content-type of 'application/json' and
    output it.
    
    """
    pylons = get_pylons(args)
    pylons.response.headers['Content-Type'] = 'application/json'
    data = func(*args, **kwargs)
    if isinstance(data, (list, tuple)):
        msg = "JSON responses with Array envelopes are susceptible to " \
              "cross-site data leak attacks, see " \
              "http://pylonshq.com/warnings/JSONArray"
        warnings.warn(msg, Warning, 2)
        log.warning(msg)
    return jsonpickle.encode(data, unpicklable=False)

ourjsonify = decorator(ourjsonify)
