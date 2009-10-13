import urllib

from google.appengine import api

import base

URI = "http://www.worldofwarcraft.com/realmstatus/compat.html"

class Main(base.RequestHandler):

    def get(self, *args):
        realm = args[1] or ""
        if not realm:
            return self.ok("Please specify a realm.")
        realm = urllib.unquote(realm)
        response = api.urlfetch.fetch(URI).content.lower()
        token = "#660D02;\">%s" % realm.lower()
        if token in response:
            return self.ok("%s is up" % realm)
        return self.ok("%s is down" % realm)
