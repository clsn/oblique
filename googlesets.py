import urllib
import StringIO
import csv

from google.appengine import api

import base
from contrib import BeautifulSoup
import re

baseuri="http://labs.google.com/sets"

def startswithgoogle(s):
    return s.startswith("http://www.google.com/search?")

class Main(base.RequestHandler):

    def get(self, *args):
        try:
            query=base.collapse(urllib.unquote(args[1]))
        except Exception:
            return self.ok("Please provide some sample elements.")
        query=StringIO.StringIO(query)
        words=csv.reader(query, delimiter=" ").next()
        keys=map(str.__add__,['q']*5,map(str,range(1,6)))
        dct={}
        for i in range(0,5):
            try:
                dct[keys[i]]=words[i]
            except Exception:
                dct[keys[i]]=""
        dct['btn']='Small Set (15 items or fewer)'
        dct['hl']='en'
        query=urllib.urlencode(dct)
        try:
            fetch=api.urlfetch.fetch(baseuri+'?'+query)
            html=fetch.content
        except Exception:
            return self.ok("Error fetching results")
        try:
            tree = BeautifulSoup.BeautifulSoup(html)
            #convertEntities=BeautifulSoup.BeautifulStoneSoup.HTML_ENTITIES)
            links=tree.findAll("a", {"href":startswithgoogle})
            message = ", ".join(map((lambda x: x.string), links))
            if not message:
                message="Nothing found.  All lonely."
        except:
            return self.ok("Error parsing results.")        
        return self.ok(message)
