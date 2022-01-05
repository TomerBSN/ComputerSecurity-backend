import binascii
import hashlib
import os
import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def check_email(email):
    """Check if email is in format XX@YY.ZZ"""
    if re.fullmatch(regex, email):
        return True
    else:
        return False


def hash_password(password):
    """Hash a password for storing."""

    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')

    changed_salt = ""

    sicret_key = [4, 3, 6, 4, 1, 2, 5, 2, 7, 0, 7, 2, 4, 4, 8, 9, 0, 7, 8, 4, 9, 3, 7, 6, 8, 3, 3, 7, 5, 6, 7, 4, 6, 8,
                  2, 5, 9, 0, 3, 4, 9, 2, 9, 7, 5, 6, 0, 7, 2, 6, 5, 3, 6, 1, 7, 1, 0, 3, 2, 1, 0, 1, 9, 7]
    for ch, i in zip((salt).decode('ascii'), sicret_key):
        changed_salt = changed_salt + chr(ord(ch) + i)

    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    """the  hashed password with salt!!! first 64 element"""
    return (changed_salt.encode('utf-8') + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]

    changed_salt = ""

    sicret_key = [4, 3, 6, 4, 1, 2, 5, 2, 7, 0, 7, 2, 4, 4, 8, 9, 0, 7, 8, 4, 9, 3, 7, 6, 8, 3, 3, 7, 5, 6, 7, 4, 6, 8,
                  2, 5, 9, 0, 3, 4, 9, 2, 9, 7, 5, 6, 0, 7, 2, 6, 5, 3, 6, 1, 7, 1, 0, 3, 2, 1, 0, 1, 9, 7]
    for ch, i in zip(salt, sicret_key):
        changed_salt = changed_salt + chr(ord(ch) - i)

    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  changed_salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def crate_ver_key():
    # global temp_pass
    temp_pass = hashlib.sha1(os.urandom(60)).hexdigest().encode('ascii')

    # print("first :  "+str(temp_pass))

    return temp_pass.decode('ascii')


def send_email(recipient, body):
    import smtplib

    # GET THE EMAIL USER FROM THS DB
    # SEND THE BODY

    FROM = "CommunicationLTD00@gmail.com"
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = "verification code"
    TEXT = "Your verification code: \n \n " + body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(FROM, "OLeg_is_king3.14")
        server.sendmail(FROM, TO, message)
        server.close()
        print('successfully sent the mail')
    except:
        print("failed to send mail")


global users_data
users_data = {}
