import htmlentitydefs
import unicodedata
import urllib

from google.appengine import api

import base

class Main(base.RequestHandler):

    def get(self, *args):
        c = args[1] or ""
        if not c:
            return self.ok("Please provide a UTF-8 character.")
        c = urllib.unquote(c)
        try:
            u = c.decode("utf8")
        except:
            return self.ok("Error decoding UTF-8 character.")
        if len(u) > 1:
            return self.ok("Please provide only one UTF-8 character.")
        charref = "&%s;" % htmlentitydefs.codepoint2name.get(ord(u), "#x%04X" % ord(u))
        try:
            name = unicodedata.name(u)
        except:
            name = "(No name found)"
        self.ok("%s - %s" % (name, charref))
