import urllib
import StringIO

from google.appengine import api

from django.utils import simplejson

import base
from contrib import BeautifulSoup

API_URI = "http://www.searchmash.com/results/"

# @@ broken

class Main(base.RequestHandler):

    def get(self, *args):
        query = urllib.unquote(args[1])
        if not query:
            return self.ok("Please provide a domain.")
        query = StringIO.StringIO(query)
        try:
            query_tokens = csv.reader(query, delimiter=" ").next()
        except:
            return self.ok("Please use proper quoting for arguments.")
        try:
            domain = query_tokens[0] or ""
        except:
            domain = ""
        if not from_name:
            return self.ok("Please provide a domain")
        try:
            search = query_tokens[1] or ""
        except:
            search = ""
        if not to_name:
            return self.ok("Please provide a search query.")
        uri_query = urllib.quote("site:" + domain + " " + search)
        uri = API_URI + uri_query
        try:
            json = api.urlfetch.fetch(uri).content.decode("utf-8")
            json = simplejson.decode(json)
        except:
            return self.ok("Error performing search.")
        for result in json["results"]:
           uri = result["rawUrl"]
           if uri == "/":
              continue
           try:
              html = soupparser.fromstring(result["title"])
              title = html.xpath("normalize-space(/)")
           except Exception, error:
              return self.ok("Error parsing title.")
           return self.ok("%s - %s" % (title, uri))
        return self.ok("No results found.")
