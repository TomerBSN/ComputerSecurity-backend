import hashlib
import os

import null as null
from rest_framework import serializers
from .models import *
from communication_ltd.pass_config import PassConfig
from communication_ltd.useful_functions import hash_password
from communication_ltd.useful_functions import verify_password
from communication_ltd.useful_functions import send_email
from django.db import connections

cursor = connections['default'].cursor()
pass_config = PassConfig()


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
        is_exists = self.check_if_user_exists(self.data['username'])
        if is_exists:
            print('Error: user is already exists!')
            return False, 'Error: user is already exists!'

        password = self.data['password']
        is_ok, msg = self.verify_pass_by_config(password)
        if not is_ok:
            print(msg)
            return False, msg

        email = self.data['email']

        hash_salt_pwd = hash_password(password)
        cursor.execute("INSERT INTO app_user(username,password,email) VALUES( %s , %s, %s )", [username,
                                                                                               hash_salt_pwd, email])
        return True, 'OK'

    @staticmethod
    def check_if_user_exists(username):
        cursor.execute("SELECT * from app_user where username like %s", [username])
        res = cursor.fetchall()
        if len(res):
            return True
        return False

    @staticmethod
    def verify_pass_by_config(password):
        errors = []

        if len(password) < pass_config.min_length:
            errors.append(f'Password length is lower than {pass_config.min_length} chars!')

        types_counter = pass_config.count_char_types(password)
        if types_counter < pass_config.min_char_types:  # check for the minimum char types we expect
            types_group = [key for key, val in pass_config.char_types.items() if pass_config.char_types[key]]
            print(types_group)
            errors.append(f'Password must contain at least {pass_config.min_char_types} char types'
                          f' from the following group: {types_group}!')

        if pass_config.is_in_keywords_dict(password):
            errors.append('Password found in keywords dictionary!')

        if len(errors):
            return False, errors

        return True, 'OK'


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def checkLogin(self):
        # need to connect to menu

        if not UserSerializer.check_if_user_exists(self.data['username']):
            print('Error: user is not exists!')
            return False, 'Error: user is not exists!'
        password = self.data['password']
        old_pass = self.get_pas_from_db(self.data['username'])
        # print(old_psa)

        if verify_password(old_pass, password):
            return True, 'ok'
        return False, 'not ok'

    @staticmethod
    def get_pas_from_db(username):
        cursor.execute("SELECT password from app_user where username like %s", [username])
        res = cursor.fetchall()
        for row in res:
            old_pas = row[0]

        return old_pas


class ForgotPassSerializer(serializers.ModelSerializer):
    # code = serializers.CharField()
    class Meta:
        model = User
        fields = ['username']
    temp_pass= null

    def send_tamp_password(self):
        # check user

        if not UserSerializer.check_if_user_exists(self.data['username']):
            return False, 'Error: user is already exists!'
        temp_pass = hashlib.sha1(os.urandom(60)).hexdigest().encode('ascii')
        # SAVE TO TEMP DB
        username = self.data['username']
        # if not UserSerializer.check_if_user_exists(self.data['username']):
        #     cursor.execute("INSERT INTO temp_pass(username,password) VALUES( %s , %s )", [username, temp_password])
        # else:
        #     cursor.execute("UPDATE INTO temp_pass(username,password) VALUES( %s , %s )", [username, temp_password])
        #
        user_email = self.get_email_of_user_from_db(username)
        send_email(user_email,str(temp_pass))
        return True,'ok'
        # SAVE TO TEMP DB
        # MESS="YOUR TEMP PASS IS ,TEMP PASS"
        # CONNECT TO A NEW WINDOW WITH TWO LINES(USER ,PASSWORD) TO INSERT THE TEMP PASS.
        # CONNECT TO CHANGE PASS




    # def verify_temp_pass(self):
    #
    #     # if input == temp pass connect to change pass
    #     # else throw exception
    #

    @staticmethod
    def get_email_of_user_from_db(username):
        cursor.execute("SELECT email from app_user where username like %s", [username])
        res = cursor.fetchall()
        for row in res:
            email = row[0]

        return email

class ChangePassSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField()

    class Meta:
        model = User
        fields = ['password', 'new_password']


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
