import csv
import StringIO
import urllib

from google.appengine import api

import base
from contrib import BeautifulSoup
from contrib import unescape

API_URI = "http://www.netsoc.tcd.ie/~mu/cgi-bin/shortpath.cgi"

class Main(base.RequestHandler):

    def get(self, *args):
        query = base.collapse(urllib.unquote(args[1]))
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
            html = api.urlfetch.fetch(uri).content
            html = unescape.unescape(html.decode("latin1"))
            tree = BeautifulSoup.BeautifulSoup(html)
        except Exception, error:
            return self.ok("Timeout fetching Wikipedia distance.")
        try:
            messages = []
            for a in tree.findAll("a"):
                messages.append(base.collapse(a.string))
            messages = messages[1:]
        except:
            return self.ok("Could not find Wikipedia distance.")
        if not messages:
            try:
                self.ok(tree.find("b").string + ".")
            except:
                try:
                    self.ok(tree.find("h2").string + ".")
                except:
                    self.ok("Error parsing Wikipedia distance.")
        message = " > ".join(messages)
        return self.ok(message)
