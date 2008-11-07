import urllib

from google.appengine import api

import base
from contrib import BeautifulSoup
import re

basuri="http://labs.google.com/sets"

def startswithgoogle(s):
    return s.startswith("http://www.google.com/search?")

class Main(base.RequestHandler):

    def get(self, *args):
        words=map(urllib.unquote, args[1:6])
        if not words:
            self.ok("Please provide some sample elements.")
        keys=map(str.__add__,['q']*5,map(str,range(1,5)))
        dct={}
        for i in range(0,5):
            try:
                dct[keys[i]]=words[i]
            except Exception:
                dct[keys[i]]=""
        dct['btn']='Small Set (15 items or fewer)'
        try:
            fetch=api.urlfetch(baseuri,method=api.urlfetch.GET,
                               payload=payload)
            html=fetch.content
        except Exception:
            return self.ok("Error fetching results")
        try:
            tree = BeautifulSoup.BeautifulSoup(html)
            #convertEntities=BeautifulSoup.BeautifulStoneSoup.HTML_ENTITIES)
            links=tree.findAll("a", {"href":startswithgoogle})
            message = ", ".join(map((lambda x: x.string), links))
        except:
            return self.ok("Error parsing results.")        
        return self.ok(message)
