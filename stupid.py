import re
import StringIO
import urllib

from google.appengine import api

import base

from contrib import BeautifulSoup
from contrib import html2text

API_URI = "http://stupidfilter.org/demo.php"

class Main(base.RequestHandler):

    def get(self, *args):
        uri = args[1]
        if not uri:
            self.ok("Please provide a URI.")
        uri = urllib.unquote(uri)
        try:
            html = api.urlfetch.fetch(uri).content
            tree = BeautifulSoup.BeautifulSoup(html)
            html = tree.prettify().decode("utf8")
            text = html2text.html2text(html).encode("utf8")
        except Exception:
            return self.ok("Error fetching URI.")
        text = base.collapse(re.sub("\W|\d", " ", text))
        payload = urllib.urlencode({"data": text})
        try:
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            html = api.urlfetch.fetch(
                API_URI,
                method=api.urlfetch.POST,
                payload=payload,
                headers=headers).content
        except Exception:
            return self.ok("Error fetching URI results.")
        tree = BeautifulSoup.BeautifulSoup(html)
        try:
            message = base.collapse(tree.find("b").string)
        except:
            return self.ok("Error parsing results.")
        return self.ok(message)
