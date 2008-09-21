import unicodedata
import urllib

from google.appengine import api

import base

URI = "http://www.fileformat.info/info/unicode/char/%04X/index.htm"

class Main(base.RequestHandler):

    def get(self, *args):
        character = args[1] or ""
        if not character:
            return self.ok("Please provide a UTF-8 character.")
        character = urllib.unquote(character)
        try:
            unicode = character.decode("utf8")
        except:
            return self.ok("Error decoding UTF-8 character.")
        if len(unicode) > 1:
            return self.ok("Please provide only one UTF-8 character.")
        self.ok("%s - %s" % (unicodedata.name(unicode[0]), URI % ord(unicode[0])))
