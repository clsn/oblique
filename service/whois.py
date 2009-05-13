import urllib
from xml.etree import ElementTree

from google.appengine import api

import base

API_URI = "http://www.trynt.com/whois-api/v1/"

class Main(base.RequestHandler):

    def get(self, *args):
        domain = args[1] or ""
        if not domain:
            return self.ok("Please provide a domain name.")
        domain = urllib.unquote(domain).split()
        if len(domain) > 1:
            return self.ok("Please provide a single domain name.")
        domain = domain[0]
        query = urllib.urlencode({"h": domain, "f": 0})
        uri = API_URI + "?" + query
        try:
            tree = ElementTree.XML(api.urlfetch.fetch(uri).content)
        except Exception, error:
            return self.ok("Invalid API response.")
        registered = tree.find(".//regrinfo/registered")
        if registered.text.strip() == "no":
            return self.ok("The %s domain is not registered." % domain)
        message = "The %s domain is registered" % domain
        try:
            message += " to %s" % base.collapse(tree.find(".//owner/name").text)
        except:
            pass
        if message[-1] != ".":
            message += "."
        return self.ok(message.encode("utf8"))
