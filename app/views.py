from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from . serializers import *
from communication_ltd.useful_functions import users_data
from django.contrib.auth import signals
from communication_ltd.decorators import axes_dispatch, auth_gateway, verify_gateway, change_pass_fp_gateway


# ----------------------------------------Views----------------------------------------

class RegisterView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            save_status, msg = serializer.save()
            if save_status:
                users_data['username'] = request.data['username']
                users_data['authenticated'] = True
                return Response({"Success": "User data saved!"}, status=status.HTTP_200_OK)
            return Response({"Fail": msg}, status=status.HTTP_200_OK)


@method_decorator(axes_dispatch, name='dispatch')
class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            check_status, msg = serializer.check_login()
            if check_status:            # True if user credentials are correct
                users_data['username'] = request.data['username']
                users_data['authenticated'] = True

                return Response({"Success": msg},  status=status.HTTP_200_OK)    # after user is logged in, refer to menu page

            # if user failed to log in, send user_login_failed signal
            signals.user_login_failed.send(sender=User, request=request,
                                           credentials={'username': request.data['username'], },)
            users_data['authenticated'] = False
            return Response({"Fail": msg}, status=status.HTTP_200_OK)


class ForgotPassView(APIView):
    serializer_class = ForgotPassSerializer

    def post(self, request):
        serializer = ForgotPassSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            check_status, msg = serializer.send_ver_key()
            if check_status:
                users_data['username'] = request.data['username']
                users_data['ver_key'] = msg
                users_data['fp_verify'] = True
                return Response({"Success": "successfully sent the mail"},  status=status.HTTP_200_OK)

            return Response({"Fail": msg}, status=status.HTTP_200_OK)


@method_decorator(verify_gateway, name='dispatch')
class VerifyView(APIView):
    serializer_class = VerifyForgotPass

    def post(self, request):
        serializer = VerifyForgotPass(data=request.data)
        if serializer.is_valid(raise_exception=True):
            check_status, msg = serializer.verify_ver_key(users_data['ver_key'])
            if check_status:
                users_data['verified'] = True
                users_data['ver_key'] = request.data['verify']
                return Response({"Success": msg},  status=status.HTTP_200_OK)

            users_data['verified'] = False
            return Response({"Fail": msg}, status=status.HTTP_200_OK)


@method_decorator(auth_gateway, name='dispatch')
class ChangePassView(APIView):
    serializer_class = ChangePassSerializer

    def post(self, request):
        serializer = ChangePassSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            save_status, msg = serializer.change_pass(users_data['username'])
            if save_status:
                return Response({"Success": "User password has changed!"}, status=status.HTTP_200_OK)
            return Response({"Fail": msg}, status=status.HTTP_200_OK)


@method_decorator(change_pass_fp_gateway, name='dispatch')
class ForgetPassChangePassView(APIView):
    serializer_class = ChangePassForForgotPassSerializer

    def post(self, request):
        serializer = ChangePassForForgotPassSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            save_status, msg = serializer.change_pass(users_data['username'])
            if save_status:
                users_data['fp_verify'] = False
                users_data['verified'] = False
                del users_data['ver_key']
                return Response({"Success": "User password has changed!"}, status=status.HTTP_200_OK)
            return Response({"Fail": msg}, status=status.HTTP_200_OK)


@method_decorator(auth_gateway, name='dispatch')
class AddCustomerView(APIView):
    serializer_class = CustomerSerializer

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            save_status, msg = serializer.save_customer(users_data['username'])
            if save_status:
                return Response({"Success": msg}, status=status.HTTP_200_OK)
            return Response({"Fail": msg}, status=status.HTTP_200_OK)


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


@auth_gateway
def logout(request):
    request.session.flush()
    return HttpResponseRedirect('/login/')
