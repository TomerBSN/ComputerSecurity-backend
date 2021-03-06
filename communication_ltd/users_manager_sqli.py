from django.db import connections
import datetime
from communication_ltd.useful_functions import verify_password, hash_password


class UsersManagerSqli:     # Same logic as UsersManager but with vulnerable sql queries
    def __init__(self):
        self.cursor = connections['default'].cursor()

    def check_if_user_exists(self, username):
        self.cursor.execute(f"SELECT username from app_user where username like " + f"'{username}'")
        res = self.cursor.fetchall()
        if len(res):
            return True
        return False

    def save_user_on_db(self, username, password, email):
        hash_salt_pwd = hash_password(password)              # make hash+halt
        self.cursor.execute("INSERT INTO app_user(username,password,email) VALUES( " + f"'{username}'" +
                            ", " + f"'{hash_salt_pwd}'" + ", " + f"'{email}')")

    def verify_user_password(self, username, password):
        old_pass = self.get_pass_from_db(username)
        # check if the password entered by the client is matching to the password (hash+salt) saved in users DB
        if verify_password(old_pass, password):
            return True
        return False

    def get_pass_from_db(self, username):
        self.cursor.execute("SELECT password from app_user where username like " + f"'{username}'")
        res = self.cursor.fetchall()
        return res[0][0]

    def get_email_of_user_from_db(self, username):
        self.cursor.execute("SELECT email from app_user where username like " + f"'{username}'")
        res = self.cursor.fetchall()
        return res[0][0]

    def set_new_password(self, username, new_hash_salt_pwd):
        self.cursor.execute('UPDATE app_user SET password = ' + f"'{new_hash_salt_pwd}'" +
                            ' WHERE username = ' + f"'{username}'")

    def save_pwd_on_history(self, username, pwd):
        d = datetime.datetime.now()
        date = f'{d.day}_{d.month}_{d.year}_{d.hour}_{d.minute}_{d.second}'
        self.cursor.execute("INSERT INTO app_passhistory(username,password,date) VALUES( " + f"'{username}'" +
                            ", " + f"'{pwd}'" + ", " + f"'{date}')")

    def get_passwords_history(self, username, history):
        self.cursor.execute("SELECT password from app_passhistory where username like " + f"'{username}'")
        res = self.cursor.fetchall()
        if len(res):
            passwords_history = list(map(lambda x: x[0], res))[::-1]
            if len(passwords_history) > history:     # if there are more passwords than history limit, than remove them
                passwords_to_remove = passwords_history[history:]
                for password in passwords_to_remove:
                    self.cursor.execute("DELETE from app_passhistory where password like " + f"'{password}'")
            return passwords_history[:history]
        return []

    def check_history_passwords(self, username, new_password, history):
        curr_hash_salt_password = self.get_pass_from_db(username)
        if history and verify_password(curr_hash_salt_password, new_password):
            return False, f'Error: you cant use your last {history} previous passwords!'
        if history > 1:     # if history > 1 check the oldest passwords in passwords history table
            h_passwords = self.get_passwords_history(username, history-1)
            if len(h_passwords):    # check if the user has history passwords (more than 1)
                for h_pass in h_passwords:
                    if verify_password(h_pass, new_password):     # compare the new passwords to all history passwords
                        return False, f'Error: you cant use your last {history} previous passwords!'

        new_hash_salt_password = hash_password(new_password)
        self.set_new_password(username, new_hash_salt_password)      # save the new passwords in users table
        self.save_pwd_on_history(username, curr_hash_salt_password)  # copy the last password in passwords history table
        return True, 'ok'

    def add_customer(self, customer_name, customer_last_name, customer_email, added_by):
        self.cursor.execute(f"INSERT INTO app_customer(first_name,last_name,email,added_by) select "
                            f"\'{customer_name}\', \'{customer_last_name}\', \'{customer_email}\', \'{added_by}\'")

    def get_customer(self, customer_name, customer_last_name):
        self.cursor.execute("SELECT first_name, last_name from app_customer where first_name like " +
                            f"'{customer_name}'" + " and last_name like " + f"'{customer_last_name}'")
        res = self.cursor.fetchall()
        return res


users_manager = UsersManagerSqli()
