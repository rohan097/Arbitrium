from controllers.modules import *

class LogoutHandler(RequestHandler):

    """
	class resposible to handle the logout functions

	route : /logout
	"""

    @removeslash
    @coroutine
    def get(self):

        token = self.get_secure_cookie('token')
        if token:
            self.clear_cookie('token')
            self.redirect('/login?loggedOut=true')

        else:
            self.redirect('/login?activesession=false')
