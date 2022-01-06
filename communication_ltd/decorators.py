from functools import wraps
from axes.handlers.proxy import AxesProxyHandler
from axes.helpers import get_lockout_response
from communication_ltd.useful_functions import users_data
from rest_framework.response import Response
from rest_framework import status

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
        if 'authenticated' in users_data and users_data['authenticated']:
            return func(request, *args, **kwargs)

        return Response({"Fail": "No access"}, status=status.HTTP_200_OK)

    return inner


def verify_gateway(func):
    # This is the verify page session decorator, in order to avoid unattended user to access this page
    @wraps(func)
    def inner(request, *args, **kwargs):
        if 'fp_verify' in users_data and users_data['fp_verify']:
            return func(request, *args, **kwargs)

        return Response({"Fail": "No access"}, status=status.HTTP_200_OK)

    return inner


def change_pass_fp_gateway(func):
    # This is the change_pass (after forget pass) session decorator,
    # user can access this page only if the key sent by email is verified
    @wraps(func)
    def inner(request, *args, **kwargs):
        if 'verified' in users_data and users_data['verified']:
            return func(request, *args, **kwargs)

        return Response({"Fail": "No access"}, status=status.HTTP_200_OK)

    return inner
