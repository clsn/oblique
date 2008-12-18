from google.appengine import api

import base
import urllib

class Main(base.RequestHandler):

    def get(self, *args):
        return self.ok("This is boring: "+urllib.unquote(args[1]))
