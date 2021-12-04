from rest_framework import serializers
from .models import *
from django.db import connections
cursor = connections['default'].cursor()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def save(self):
        """
        save user details to into app_user table
        :return:
        """
        username = self.data['username']
        password = self.data['password']
        email = self.data['email']
        cursor.execute("INSERT INTO app_user(username,password,email) VALUES( %s , %s, %s )", [username,
                                                                                               password, email])


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name']

    def save(self):
        """
        place holder - need to implement here SQL query
        :return:
        """
        print(self.data)
