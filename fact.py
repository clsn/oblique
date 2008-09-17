import urllib
from xml.dom import minidom

from google.appengine import api

import base

class Main(base.RequestHandler):

    def get(self, *args):
        uri = args[1] or ""
        if not uri:
            return self.ok("Please specify a URI.")
        uri = urllib.unquote(uri)
        if not uri.startswith("http://"):
            uri = "http://" + uri
        try:
            tree = minidom.parseString(api.urlfetch.fetch(uri).content)
        except Exception, error:
            return self.ok("Error fetching new fact.")
        for element in tree.getElementsByTagName("p"):
            if element.getAttribute("class") == "fact":
                return self.ok(base.text(element))
