import urllib

from google.appengine import api

import base

URI = "http://www.worldofwarcraft.com/realmstatus/compat.html"

class Main(base.RequestHandler):

    def get(self, *args):
        realm = args[1] or ""
        if not realm:
            return self.ok("Please specify a realm.")
        realm = urllib.unquote(realm).lower()
        response = api.urlfetch.fetch(URI).content.lower()
        if realm not in response:
            return self.ok("That breaks science")
        token = "#660d02;\">%s" % realm
        if token in response:
            return self.ok("%s is down" % realm.title())
        return self.ok("%s is up" % realm)


