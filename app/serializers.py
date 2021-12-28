import hashlib
import os
from rest_framework import serializers
from .models import *
from communication_ltd.pass_config import pass_config
from communication_ltd.users_manager import users_manager
from communication_ltd.useful_functions import send_email


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def save(self):
        """
        save user details to into app_user table
        :return: bool, status msg
        """
        username = self.data['username']
        # check if username entered by the client is already exists in users table
        is_exists = users_manager.check_if_user_exists(self.data['username'])
        if is_exists:
            print('Error: user is already exists!')
            return False, 'Error: user is already exists!'

        password = self.data['password']
        # verify that the new password entered by the client is valid (according to passwords config file)
        is_ok, msg = pass_config.verify_pass_by_config(password)
        if not is_ok:
            return False, msg

        email = self.data['email']

        users_manager.save_user_on_db(username, password, email)   # save hash_salt_password in users table

        return True, 'OK'


class LoginSerializer(serializers.ModelSerializer):
    """
    make user login authentication
    :return: bool, status msg
    """
    class Meta:
        model = User
        fields = ['username', 'password']

    def check_login(self):
        # check if username entered by the client is exists in users table
        username = self.data['username']
        if not users_manager.check_if_user_exists(self.data['username']):
            print('Error: user is not exists!')
            return False, 'Error: wrong credentials!'
        password = self.data['password']

        # check if the password entered by the client is matching to the password (hash+salt) saved in users DB
        if users_manager.verify_user_password(username, password):
            return True, 'Login successfully!'
        return False, 'Error: wrong credentials!'


class ForgotPassSerializer(serializers.ModelSerializer):
    # code = serializers.CharField()
    class Meta:
        model = User
        fields = ['username']
    temp_pass = None

    def send_tamp_password(self):
        # check user

        if not users_manager.check_if_user_exists(self.data['username']):
            return False, 'Error: user is already exists!'
        temp_pass = hashlib.sha1(os.urandom(60)).hexdigest().encode('ascii')
        # SAVE TO TEMP DB
        username = self.data['username']
        # if not users_manager.check_if_user_exists(self.data['username']):
        #     cursor.execute("INSERT INTO temp_pass(username,password) VALUES( %s , %s )", [username, temp_password])
        # else:
        #     cursor.execute("UPDATE INTO temp_pass(username,password) VALUES( %s , %s )", [username, temp_password])
        #
        user_email = users_manager.get_email_of_user_from_db(username)
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


class ChangePassSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField()

    class Meta:
        model = User
        fields = ['password', 'new_password']

    def change_pass(self, username):
        """
        verify new_password is valid, if so save it in users table
        :return: bool, status msg
        """

        # verify that the current password entered by the user is OK
        entered_password = self.data['password']
        if not users_manager.verify_user_password(username, entered_password):
            return False, 'Error: your current password is wrong!'

        # verify that the new password entered by the user is valid (according to passwords config file)
        new_password = self.data['new_password']
        is_ok, msg = pass_config.verify_pass_by_config(new_password)
        if not is_ok:
            return False, msg

        return users_manager.check_history_passwords(username, new_password, pass_config.history)


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
