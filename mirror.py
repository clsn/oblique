import random
import urllib

from google.appengine import api

import base
from contrib import BeautifulSoup

INSULT_URI = "http://trevorstone.org/curse/curse.php?number=1"

COMPLIMENT_URI = "http://www.madsci.org/cgi-bin/cgiwrap/~lynn/jardin/SCG"

class Main(base.RequestHandler):

    def get(self, *args):
        if random.randint(0, 1):
            soup = BeautifulSoup.BeautifulSoup(api.urlfetch.fetch(INSULT_URI).content)
            text = soup.findAll('body')[0].find(recursive=False, text=True)
        else:
            soup = BeautifulSoup.BeautifulSoup(api.urlfetch.fetch(COMPLIMENT_URI).content)
            text = soup.findAll('h2')[0].find(recursive=False, text=True)
        return self.ok(" ".join(text.split()))
