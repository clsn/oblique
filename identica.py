from xml.dom import minidom

from google.appengine import api

import base

class Main(base.RequestHandler):

    def get(self, *args):
        user = args[1] or ""
        if not user:
            return self.ok("Please provide a username.")
        try:
            xml = api.urlfetch.fetch("http://identi.ca/%s/rss" % user).content
            doc = minidom.parseString(xml)
        except:
            return self.ok("Error parsing user feed.")
        try:
            text = doc.getElementsByTagName('title')[2].firstChild.nodeValue
        except:
            return self.ok("No posts found." % user)
        return self.ok(text)
