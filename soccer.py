from google.appengine import api

from xml.dom.minidom import parseString

import base, re, urllib

class Main(base.RequestHandler):

    def get(self, *args):

        source = "http://www.scorespro.com/rss/live-soccer.xml"
        
        text = args[1] or ""

        if not text:
            return self.ok("Please specify a team.")

        text = urllib.unquote(text)
        regexp = re.compile("^.*%s.*$" % text, re.IGNORECASE)
        doc = parseString(api.urlfetch.fetch(source).content)

        for entry in doc.getElementsByTagName("title")[1:-1]:
            scoreline = entry.childNodes[0].toxml()
            if regexp.match(scoreline):
                return self.ok(scoreline)

        self.ok("No score was found for your query '%s'!" % text)

