from functools import wraps
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from . serializers import *
from axes.decorators import axes_dispatch
from django.contrib.auth import signals


def auth_gateway(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        if 'authenticated' in request.session and request.session['authenticated']:
            return func(request, *args, **kwargs)

        return HttpResponseRedirect('/login/')

    return inner


class RegisterView(APIView):
    serializer_class = UserSerializer

    # def get(self, request):
    #     detail = [{"username": detail.username, "pass": detail.password, "email":detail.email}
    #               for detail in User.objects.all()]
    #     return Response(detail)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            save_status, msg = serializer.save()
            if save_status:
                return Response({"Success": "User data saved!"}, status=status.HTTP_200_OK)
            return Response({"Fail": msg}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(axes_dispatch, name='dispatch')
class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            check_status, msg = serializer.check_login()
            if check_status:            # True if user credentials are correct
                request.session['authenticated'] = True
                request.session['username'] = request.data['username']
                request.session.set_expiry(1800)            # 30 minutes login session
                return HttpResponseRedirect('/menu/')       # after user is logged in, refer to menu page

            # if user failed to log in, send user_login_failed signal
            signals.user_login_failed.send(sender=User, request=request,
                                           credentials={'username': request.data['username'], },)
            request.session['authenticated'] = False
            return Response({"Fail": msg}, status=status.HTTP_400_BAD_REQUEST)


class ForgotPassView(APIView):
    serializer_class = ForgotPassSerializer

    def post(self, request):
        serializer = ForgotPassSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            check_status, msg = serializer.send_tamp_password()
            if check_status:
                return Response({"Success": "the email was send !"}, status=status.HTTP_200_OK)

            return Response({"Fail": msg}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(auth_gateway, name='dispatch')
class ChangePassView(APIView):
    serializer_class = ChangePassSerializer

    def post(self, request):
        serializer = ChangePassSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            save_status, msg = serializer.change_pass(request.session['username'])
            if save_status:
                return Response({"Success": "User password has changed!"}, status=status.HTTP_200_OK)
            return Response({"Fail": msg}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(auth_gateway, name='dispatch')
class AddCustomerView(APIView):
    serializer_class = CustomerSerializer

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)


def main_view(request):
    current_url = request.build_absolute_uri()
    return HttpResponse(f"<h2><p><a href=\"{current_url}register\">Register</a></p>"
                        f"<p><a href=\"{current_url}login\">Login</a></p>"
                        f"<p><a href=\"{current_url}forgot_pass\">ForgotPass</a><br<br></p></h2>")


@auth_gateway
def menu(request):
    current_url = request.build_absolute_uri()
    return HttpResponse(f"<h2><p><a href=\"{current_url}change_pass\">Change Password</a></p>"
                        f"<p><a href=\"{current_url}add_customer\">Add customer</a></p></h2>")


def logout(request):
    request.session.flush()
    return HttpResponseRedirect('/login/')
