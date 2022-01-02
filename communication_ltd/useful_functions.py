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
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    """the  hashed password with salt!!! first 64 element"""
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


temp_pass = None


def crate_one_time_pass():
    global temp_pass
    temp_pass = hashlib.sha1(os.urandom(60)).hexdigest().encode('ascii')

    print("first :  "+str(temp_pass))

    return str(temp_pass)


def verify_one_time_pass(user_temp_pass):
    global temp_pass
    if(str(user_temp_pass)==str(temp_pass)):
        return True
    return False


username_tamp = None


def tamp_save_username_for_chang_pass(username):
    global username_tamp
    username_tamp = username


def tamp_send_username_for_chang_pass():
    global username_tamp
    return username_tamp


def send_email(recipient, body):
    import smtplib

    # GET THE EMAIL USER FROM THS DB
    # SEND THE BODY

    FROM = "CommunicationLTD00@gmail.com"
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = "temp password"
    TEXT = "YOUR TEMP PASS IS:  \n \n               " + body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(FROM, "need to ask oleg ")
        server.sendmail(FROM, TO, message)
        server.close()
        print('successfully sent the mail')
    except:
        print("failed to send mail")
