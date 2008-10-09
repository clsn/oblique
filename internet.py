import re
import StringIO
import urllib

from google.appengine import api

import base

from contrib import BeautifulSoup
from contrib import unescape

API_URI = "http://voiceoftheinter.net/"

class Main(base.RequestHandler):

    def get(self, *args):
        word = args[1]
        if not word:
            self.ok("Please provide a word.")
        word = urllib.unquote(word)
        payload = urllib.urlencode({"q": word})
        try:
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            html = api.urlfetch.fetch(
                API_URI,
                method=api.urlfetch.POST,
                payload=payload,
                headers=headers).content
        except Exception:
            return self.ok("Error fetching results.")
        tree = BeautifulSoup.BeautifulSoup(html)
        try:
            message = base.collapse(tree.find("blockquote").string)
            message = unescape.unescape(message)
        except:
            return self.ok("Error parsing results.")
        return self.ok(message)
