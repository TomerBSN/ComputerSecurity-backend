from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['username', 'password']
        fields = ['username', 'password', 'email']

    def save(self):
        """
        place holder - need to implement here SQL query
        :return:
        """
        print(self.data)


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
