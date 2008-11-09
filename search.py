import csv
import urllib
import StringIO

from google.appengine import api

from django.utils import simplejson

import base
from contrib import html2text

API_URI = "http://www.searchmash.com/results/"

class Main(base.RequestHandler):

    def get(self, *args):
        search = args[1]
        if not search:
            return self.ok("Please provide a search query.")
        uri = API_URI + urllib.quote(urllib.unquote(search))
        try:
            json = api.urlfetch.fetch(uri).content.decode("utf-8")
            json = simplejson.loads(json)
        except:
            return self.ok("Error performing search.")
        for result in json["results"]:
           uri = result["rawUrl"]
           if uri == "/":
              continue
           try:
              title = " ".join(html2text.html2text(result["title"]).split())
           except Exception, error:
              return self.ok("Error parsing title.")
           return self.ok("%s - %s" % (title, uri))
        return self.ok("No results found.")
