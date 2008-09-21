import csv
import StringIO
import urllib

from google.appengine import api

import base
from contrib import BeautifulSoup

API_URI = "http://www.netsoc.tcd.ie/~mu/cgi-bin/shortpath.cgi"

class Main(base.RequestHandler):

    def get(self, *args):
        query = urllib.unquote(args[1])
        if not query:
            return self.ok("Please provide two Wikipedia article titles.")
        query = StringIO.StringIO(query)
        try:
            query_tokens = csv.reader(query, delimiter=" ").next()
        except:
            return self.ok("Please use proper quoting for arguments.")
        try:
            from_name = query_tokens[0] or ""
        except:
            from_name = ""
        if not from_name:
            return self.ok("Please name a starting Wikipedia article title.")
        try:
            to_name = query_tokens[1] or ""
        except:
            to_name = ""
        if not to_name:
            return self.ok("Please name an ending Wikipedia article title.")
        query = urllib.urlencode({"from": from_name, "to": to_name})
        uri = API_URI + "?" + query
        try:
            tree = BeautifulSoup.BeautifulSoup(api.urlfetch.fetch(uri).content)
        except:
            return self.ok("Error fetching Wikipedia distance.")
        try:
            messages = []
            for a in tree.findAll("a"):
                messages.append(base.collapse(a.string))
            messages = messages[1:]
        except:
            return self.ok("Could not find Wikipedia distance.")
        if not messages:
            self.ok(tree.find("b").string + ".")
        message = " > ".join(messages)
        return self.ok(message)
