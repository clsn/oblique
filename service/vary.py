import urllib
import re

from google import appengine
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
        headers = {"Negotiate": "trans", "Accept": ""}
        try:
            response = api.urlfetch.fetch(uri, headers=headers)
        except:
            return self.ok("Unable to dereference URI.")
        if response.status_code not in (300, 406):
            return self.ok("Response was %d, expected 300 or 406." % response.status_code)
        alternates = response.headers.get("alternates")
        if not alternates:
            return self.ok("Resource does not support transparent content negotiation.")
        alternates =  re.compile("\"([^\"]+)\"").findall(alternates)
        if not alternates:
            return self.ok("Resource negotiates but no variants found.")
        if len(alternates) == 1:
            return self.ok("Single variant: %s" % alternates[0])
        else:
            return self.ok("Multiple variants: %s" % ", ".join(alternates))
        vary = response.headers.get("vary")
        if vary:
            return self.ok("Resource claims to vary on: %s" % vary)
        else:
            return self.ok("Resource does not vary.")
