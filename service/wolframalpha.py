import BeautifulSoup
import html2text
import re
import StringIO
import urllib

from google.appengine import api

import base


API_URI = "http://www39.wolframalpha.com/input/?asynchronous=false&"

class Main(base.RequestHandler):

    def get(self, *args):
        
        query = urllib.unquote(args[1])
        query = urllib.unquote_plus(query)
        query = urllib.urlencode({"i": query})
        
        if not query:
            return self.ok("Please provide a query or Wolfram will crush you with his ego.")
        
        uri = API_URI + query 
        
        try:
            html = api.urlfetch.fetch(uri,deadline=10).content
            tree = BeautifulSoup.BeautifulSoup(html)
        except Exception:
            return self.ok("Error fetching URI.")
        
        html = tree.prettify().decode("utf8")
    
        
        if re.search('sure what to do with your input', html):
            rel = tree.findAll(id="relatedInputs")
            try: 
                sugs = rel[0].findAll('a')  
                sugstr = ' '.join([anchor.contents[0] for anchor in sugs])

            except Exception:
                return self.ok("Wolfrafail: no results and couldn't parse any suggestions.\n")
             
            return self.ok("Couldn't handle your query. Suggestions: " + sugstr + "\n")
           
        found = ';'.join(re.findall('"stringified":\s"([^"]+)"', html))
        
        if not found : 
            return self.ok("Couldn't grab results from json stringified precioussss.") 

        results = found.replace('\\n',', ').replace(' | ','->')        
                      
        return self.ok(results)


