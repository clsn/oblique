import htmlentitydefs
import unicodedata
import urllib
import BeautifulSoup

from google.appengine import api

import base

class Main(base.RequestHandler):

    def get(self, *args):
        arg=args[0].split('/')[1] # starts with a slash...
        ch=arg.strip()[0].upper()
        pg=urllib.quote(urllib.unquote(arg.strip()).replace(' ','-').lower())
        url="http://www.catb.org/jargon/html/" + ch + "/" + pg + ".html"
        data=api.urlfetch.fetch(url)
        try:
            tree=BeautifulSoup.BeautifulSoup(data.content,
                                             convertEntities=BeautifulSoup.BeautifulStoneSoup.HTML_ENTITIES)
        except:
            return self.ok("Error fetching "+url)
        try:
            p=tree.find("p")
            message=base.collapse("".join(p.findAll(text=True)))
        except:
            return self.ok("Could not find definition.")
        return self.ok(message)
                               
