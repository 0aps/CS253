"""A simple webapp2 server."""

import webapp2
import re

class MainPage(webapp2.RequestHandler):

    hi = open("Login/page.html").read()
    error = {"u": "", "user": "", "password": "", "verify": "", "email": ""}

    def valid_username(self,username):
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        return USER_RE.match(username)

    def valid_password(self, passw):
        USER_RE = re.compile(r"^.{3,20}$")
        return USER_RE.match(passw)

    def valid_email(self, email):
        USER_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
        return USER_RE.match(email)

    def verify_session(self, user, passw, passw2, email):
        self.error = {"u": "", "user": "", "password": "", "verify": "", "email": ""}
        
        if not self.valid_username(user):
            self.error["user"] = "That's not a valid username."
        
        if self.valid_password(passw) == None:
            self.error["password"] = "That wasn't a valid password."
        else:
            if passw != passw2:
                self.error["verify"] = "Your passwords didn't match."
        
        if email:
            if not self.valid_email(email):
                self.error["email"] = "That's not a valid email."

        if user and passw and not email:
            if self.error["user"] == "" and self.error["password"] == "" and self.error["verify"] == "":
                return True
            else:
                return False
        elif user and passw and email:
            if self.error["user"] == "" and self.error["password"] == "" and self.error["verify"] == "" and self.error["email"] == "":
                return True
            else:
                return False

    def escape_html(self, user):
        for caracter in user:
            if caracter == '&':
                user = user.replace('&', "&amp;")
            if caracter == ">":
                user = user.replace('>', "&gt;")
            if caracter == "<":
                user = user.replace('<', "&lt;") 
            if caracter == '"':
                user = user.replace('"', "&quot;")

        return user

    def get(self):
        self.error = {"u": "", "user": "", "password": "", "verify": "", "email": ""}
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(self.hi%self.error)

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        
        user = self.request.get("username")
        passw = self.request.get("password")
        passw2 = self.request.get("verify")
        email = self.request.get("email")

        if( self.verify_session(user, passw, passw2, email) ):
            self.response.write("yes")
        else:
            self.error["u"] = self.escape_html(user)
            self.response.write(self.hi%self.error)


class handlerForm(webapp2.RequestHandler):

    def post(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(self.request)

    def get(self):
    	q = self.request.get("q")
    	self.response.headers['Content-Type'] = 'text/plain'
    	self.response.write(q)



application = webapp2.WSGIApplication([
    ('/login', MainPage)], debug=True)
