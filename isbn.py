import BeautifulSoup
import csv
import StringIO
import unescape
import urllib

from google.appengine import api

import base

API_URI = "http://www.lookupbyisbn.com/search.aspx"

class Main(base.RequestHandler):

    def get(self, *args):
        query = base.collapse(urllib.unquote(args[1]))
        query = urllib.urlencode({"key": query, "type": "Books", "page":"1"})
        uri = API_URI + "?" + query
        try:
            html = api.urlfetch.fetch(uri).content
            html = unescape.unescape(html.decode("latin1"))
            tree = BeautifulSoup.BeautifulSoup(html)
        except Exception, error:
            return self.ok("Timeout fetching ISBN information.")
        try:
            startat=tree.find("hr", {"style": "color:Silver"})
            first=startat
            while True:
                first=first.findNext("a")
                if first["href"].startswith("itemDetail"):
                    break
        except:
            return self.ok("Could not find/parse ISBN info.")
        info={"title":"",
              "isbn":"",
              "author":"",
              "pub":""}
        try:
            info["title"]=first.string
            info["isbn"]=first.findNext("b").string
            info["author"]=first.findNext("u").string
            info["pub"]=first.findNext("i").string
        except:
            pass
        return self.ok("%(author)s, %(title)s (%(isbn)s): %(pub)s"%info)

