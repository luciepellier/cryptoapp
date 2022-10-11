import os

# Secret key used to sign session cookies in flask for protection against cookie data tampering (CSRF)
SECRET_KEY = os.urandom(32)

DEBUG = True
