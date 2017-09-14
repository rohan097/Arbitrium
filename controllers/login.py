from controllers.modules import *
from controllers.utility import *

class LoginHandler(RequestHandler):

    """
    class resposible to render the dashbaord
    route : /login
    """
    @coroutine
    @removeslash
    def get(self):
        token = self.get_secure_cookie('token')
        if token:
            _id = untokenizeCokkie(token)
            isValidtkn = yield db.tokens.find_one({"token" : token, "_uid" : _id})
            if isValidtkn:
                self.redirect("/company/ford")
            else:
                self.render("login.html", admin = False)
        else:
            self.render("login.html", admin = False)

    @coroutine
    @removeslash
    def post(self):

        email = self.get_argument("email")
        pswd = self.get_argument("pswd")
        today = datetime.now()
        data = yield db.admin.find_one({"email" : email})
        if data:
            if pbkdf2_sha256.verify(data["salt"] + pswd, data["pswd"]):
                token = tokenizeCokkie(data["_id"])
                self.set_secure_cookie('token', token)

                temp = yield db.tokens.insert({"_uid" : data["_id"],
									"time" : today,
									"token" : token})

                self.redirect("/company/ford")

            else:
                self.redirect("/login?invalid_password=True")
        else:
            self.redirect("/login?invalid_email=True")
