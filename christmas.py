import datetime
import urllib

from google.appengine import api

import base
from contrib import BeautifulSoup

URI="http://trevorstone.org/curse/curse.php?number=1"

class Main(base.RequestHandler):

    def get(self, *args):
        d = datetime.datetime.now()
        if not d.month == 12 and d.day == 25:
            soup = BeautifulSoup.BeautifulSoup(api.urlfetch.fetch(URI).content)
            return self.ok("No! %s" % soup.findAll('body')[0].find(recursive=False, text=True).strip())
        else:
            return self.ok("Yes.")

