import BeautifulSoup
import fnmatch
import urllib

from google.appengine import api

import base

class Main(base.RequestHandler):

    def get(self, *args):

        args = args[1] or ""

        if not args:
            return self.ok("Please specify a query.")

        args = urllib.unquote(args)

        base_url = "http://tinyurl.com/api-create.php?url="

        talis_url = "http://api.talis.com/tx?" + \
            "xsl-uri=http://github.com/nslater/oblique/raw/master/talis.xsl&" + \
            "xml-uri=http://api.talis.com/stores/ordnance-survey/items?" + \
            "sort%3D%26max%3D100%26query%3D" + args + "%26offset%3D0&" + \
            "content-type=text/html"

        query_url = urllib.quote(talis_url)

        url = api.urlfetch.fetch(base_url + query_url).content

        self.ok(url)
