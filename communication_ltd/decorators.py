from functools import wraps
from django.http import HttpResponseRedirect
from axes.handlers.proxy import AxesProxyHandler
from axes.helpers import get_lockout_response


# ----------------------------------------Decorators----------------------------------------

def axes_dispatch(func):
    # This is the log-in attempts decorator, in order to limit maximum log-in failures
    @wraps(func)
    def inner(request, *args, **kwargs):
        if AxesProxyHandler.is_allowed(request):
            return func(request, *args, **kwargs)

        return get_lockout_response(request)

    return inner


def auth_gateway(func):
    # This is the log-in session decorator, in order to avoid unattended user to access user pages
    @wraps(func)
    def inner(request, *args, **kwargs):
        if 'authenticated' in request.session and request.session['authenticated']:
            return func(request, *args, **kwargs)

        return HttpResponseRedirect('/login/')

    return inner
