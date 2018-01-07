# -*- coding: utf-8 -*-

""" Login controller for the katalog_py webservice """

from tg import expose, TGController
from sqlalchemy.orm import Session

class RegisterController(TGController):

    def __init__(self, engine):
        self.engine = engine

    @expose('json')
    def dbg(self,*a):
        return self.post(*a)
        
    @expose('json')
    def post(self, email):
        print "todo: check email address validity for {}".format(email)
        pwd, hash = self.generate_password_for(email)
        print "todo: send email to '{}' with password '{}'".format(email, pwd)
        print "todo: add new user to the database: email '{}', password '{}'".format(email, hash)
        return { "message": "Email with your new password has been sent to {}. Please use this password for your first login.".format(email) }
    
    @staticmethod
    def generate_password_for(email):
        from hashlib import sha256
        from random import randint

        salt1 = randint(0, 2147483647)
        salt2 = randint(0, 2147483647)

        hash = sha256("{0}{1}{2}".format(salt1, email, salt2))
        digest_base64 = hash.digest().encode("base64")

        user_password = digest_base64[5:13]
        user_password_hash = sha256(user_password).digest().encode("base64")

        return user_password, user_password_hash

class LoginController(TGController):
    register = None

    def __init__(self, engine):
        self.engine = engine
        self.register = RegisterController(engine)

    @expose('json')
    def dbg(self,*a):
        return self.post(*a)

    @expose('json')
    def post(self, email, password):
        from hashlib import sha256
        print "todo: check email address validity for {}".format(email)
        entered_password = sha256(password).digest().encode("base64")
        print "todo: search database for user with email == '{}' and password_hash == '{}'".format(email, entered_password)

        return { "success":True, "message": "Login Successful" }
    

if __name__ == "__main__":
    print RegisterController.generate_password_for("hans@glueck.org")