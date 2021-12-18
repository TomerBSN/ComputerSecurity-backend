from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from . serializers import *


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


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)


class ChangePassView(APIView):
    serializer_class = ChangePassSerializer

    def post(self, request):
        serializer = ChangePassSerializer(data=request.data)


class ForgotPassView(APIView):
    serializer_class = ForgotPassSerializer

    def post(self, request):
        serializer = ForgotPassSerializer(data=request.data)


class MenuView(APIView):
    serializer_class = CustomerSerializer

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)


def main_view(request):
    current_url = request.build_absolute_uri()
    return HttpResponse(f"<h2><p><a href=\"{current_url}register\">Register</a></p>"
                        f"<p><a href=\"{current_url}login\">Login</a></p>"
                        f"<p><a href=\"{current_url}forgot_pass\">ForgotPass</a><br<br></p></h2>")
