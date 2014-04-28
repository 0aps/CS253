"""A simple webapp2 server."""

import webapp2


class MainPage(webapp2.RequestHandler):

    hi = open("Root13/page.html").read()

    def escape_html(self, caracter):
    	if caracter == '&':
    		return "&amp;"
    	if caracter == ">":
    		return "&gt;"
    	if caracter == "<":
    		return "&lt;"
    	if caracter == '"':
    		return "&quot;"

    	return caracter


    def root13(self, cadena):

    	nueva = ""
    	for ch in cadena:
    		asci_ch = ord(ch)
    		if asci_ch >= 97 and asci_ch <= 122:
    			new_ch = asci_ch+13
    			if new_ch > 122:
    				new_ch -= 26
    			nueva += chr(new_ch)
    		
    		elif asci_ch >= 65 and asci_ch <= 90:
    			new_ch = asci_ch+13
    			if new_ch > 90:
    				new_ch -= 26
    			nueva += chr(new_ch)
    		
    		else:
    			nueva += self.escape_html(ch)

    	return nueva



    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(self.hi%"Enter the text to be encrypted.")

    def post(self):
    	meh = self.request.get("text")
    	self.response.headers['Content-Type'] = 'text/html'
    	self.response.write(self.hi%self.root13(meh))


class handlerForm(webapp2.RequestHandler):

    def post(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(self.request)

    def get(self):
    	q = self.request.get("q")
    	self.response.headers['Content-Type'] = 'text/plain'
    	self.response.write(q)



application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/testform', handlerForm),
], debug=True)
