from controllers.modules import *

class IndexHandler(RequestHandler):

    """
    class resposible to redirect to login
    route : /
    """

    @coroutine
    @removeslash
    def get(self):
        self.redirect("/login")
