import re
import hashlib, binascii

from elasticsearch import Elasticsearch

es = Elasticsearch()

PEPPER = "EN214$öüoij:;:uiztR§%$"


def user_hash_password(password: str, pepper: str, salt: str):
    """
    hash the password pepper and salt
    :param password:
    :param pepper:
    :param salt:
    :return:
    """
    # conact the pepper and password
    concat_password = pepper + password
    # convert password string to binary
    bin_password = bin(int(binascii.hexlify(concat_password), 16))
    # convert salt string to binary
    bin_salt = bin(int(binascii.hexlify(salt), 16))
    # hash the pw and salt
    dk = hashlib.pbkdf2_hmac('sha256', bin_password, bin_salt, 100000)
    return binascii.hexlify(dk)


def user_password_check(password):
    """
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    :param password: the password
    :return: the check object
    """

    # calculating the length
    length_error = len(password) < 8

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', password) is None

    # overall result
    password_ok = not (length_error or digit_error or uppercase_error or lowercase_error or symbol_error)

    return {
        'password_ok': password_ok,
        'length_error': length_error,
        'digit_error': digit_error,
        'uppercase_error': uppercase_error,
        'lowercase_error': lowercase_error,
        'symbol_error': symbol_error,
    }


def user_exists(user_name: str):
    return es.exists(index="users", doc_type='user', id=user_name)


def user_create(user_name: str, password: str):
    doc = {
        user_name: user_name,
        password: user_hash_password(password, PEPPER)
    }
    pass


def user_delete(user_name: str):
    pass


def user_update(user_name_old: str, user_name_new: str):
    pass


def user_update_password(password_old: str, password_new: str):
    pass
