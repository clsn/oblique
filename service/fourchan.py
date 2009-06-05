import urllib, re, random
import BeautifulSoup

from google.appengine import api

import base

PAGE_URI = "http://img.4chan.org/b/1.html"

class Main(base.RequestHandler):

    def get(self):        
        #try:
        data = api.urlfetch.fetch(PAGE_URI).content
        tree = BeautifulSoup.BeautifulSoup(data)
            
        imgs = tree.findAll("a")
        reImg = re.compile('http://img.4chan.org/b/src/(\d+)\.jpg')
            
        result = []

        for img in imgs:
            m = reImg.search(str(img))
            if m:
                result.append(m.group(0))
            
        #except Exception, error:
            #return self.ok("Invalid API response.")
        
        return self.ok(random.choice(result))
