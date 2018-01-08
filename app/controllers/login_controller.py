# -*- coding: utf-8 -*-

""" Login controller for the katalog_py webservice """

from tg import expose, TGController

class RegisterController(TGController):

    def __init__(self, engine):
        self.engine = engine

    @expose('json')
    def dbg(self,*a):
        return self.post(*a)
        
    @expose('json')
    def post(self, email):
        from sqlalchemy.orm import Session
        from model.login_data_model import User, Model
        Model.metadata.create_all(self.engine)
        if not LoginHelpers.validate_email(email):
            return { "success": False, "message": "{} is not a valid email address, please check your input".format(email) }
        
        pwd, hash = LoginHelpers.generate_password_for(email)

        if not LoginHelpers.send_confirmation_mail(email, pwd):
            return { "success": False, "message": "unable to send confirmation mail, please try again later." }
        
        db = Session(bind=self.engine.connect())
        db.add(User(email, hash))
        db.commit()
        db.close()

        return { "success":True, "message": "Email with your new password has been sent to {}. Please use this password for your first login.".format(email) }
    
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
        from sqlalchemy.orm import Session
        from model.login_data_model import User, Model
        if not LoginHelpers.validate_email(email):
            return { "success":False, "message": "Email address invalid, please check your input" }
        
        entered_password = sha256(password).digest().encode("base64")
        
        Model.metadata.create_all(self.engine)
        db = Session(bind=self.engine.connect())
        user_matches = db.query(User).filter_by(email=email, pw_hash=entered_password)
        db.close()

        if len(user_matches.all()) == 1:
            return { "success":True, "message": "Login Successful" }
        else:
            return { "success":False, "message": "Email or username invalid, please check your input" }
    
class LoginHelpers:
        
    @staticmethod
    def validate_email(email):
        import re
        email_regex = re.compile(r'(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])')
        email_validation = email_regex.match(email)
        return email_validation is not None and email_validation.string == email

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

    def send_confirmation_mail(email, pwd):
        try:
            import smtplib
            from email.mime.text import MIMEText

            msg = MIMEText('Your password for Maya-Sammlung.ch is {}'.format(pwd))

            msg['Subject'] = 'Maya-Sammlung.ch account confirmation'
            msg['From'] = "Maya.Sammlung.ch"
            msg['To'] = email

            s = smtplib.SMTP_SSL('smtp.gmail.com',465, "maya.sammlung@gmail.com")
            s.login("maya.sammlung@gmail.com", "some password you can ask me for if you need it...")
            s.sendmail(me, [you], msg.as_string())
            s.quit()
            return True
        except Exception as ex:
            print ex
            return False

if __name__ == "__main__":
    print LoginHelpers.validate_email("hans@glueck.org")
    print LoginHelpers.validate_email("@hans@glueck.org")
    print LoginHelpers.generate_password_for("hans@glueck.org")