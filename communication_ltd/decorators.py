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


def verify_gateway(func):
    # This is the verify page session decorator, in order to avoid unattended user to access this page
    @wraps(func)
    def inner(request, *args, **kwargs):
        if 'fp_verify' in request.session and request.session['fp_verify']:
            return func(request, *args, **kwargs)

        return HttpResponseRedirect('/forgot_pass/')

    return inner


def change_pass_fp_gateway(func):
    # This is the change_pass (after forget pass) session decorator,
    # user can access this page only if the key sent by email is verified
    @wraps(func)
    def inner(request, *args, **kwargs):
        if 'verified' in request.session and request.session['verified']:
            return func(request, *args, **kwargs)

        return HttpResponseRedirect('/verify/')

    return inner