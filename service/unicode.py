import unicodedata
import urllib
import re

from google.appengine import api

import base

URI = "http://www.fileformat.info/info/unicode/char/%05X/"

class Main(base.RequestHandler):

    def get(self, *args):
        character = args[1] or ""
        if not character:
            return self.ok("Please provide a UTF-8 character.")
        character = urllib.unquote(character)
        try:
            unicode = character.decode("utf8")
        except:
            return self.ok("Error decoding UTF-8 character.")
        if len(unicode) > 1:
            return self.ok("Please provide only one UTF-8 character.")
        try:
            name = unicodedata.name(unicode[0])
        except:
            # Our unicodedata was lacking; let's ask fileformat.info
            import html5lib, xpath, StringIO
            url=URI%ord(unicode[0])
            bytes=api.urlfetch.fetch(url).content
            fp=StringIO.StringIO(bytes)
            pars=None
            try:
                pars=html5lib.parse(fp, treebuilder="dom")
            except Exception, e:
                name = "(No name found)"
            if not pars:
                name = "(No name found)"
            else: 
                con=xpath.XPathContext()
                con.namespaces["x"]="http://www.w3.org/1999/xhtml"
                it=con.find("//x:title//text()", pars.documentElement)
                if not it:
                    name="(No name found)"
                else:
                    name=reduce((lambda x,y: x+y), map((lambda x: x.data), it))
                    name=" ".join(name.split())
                    m=re.search(r"'(.*?)'", name)
                    if m:
                        name=m.group(1)
        self.ok("%s - %s" % (name, URI % ord(unicode[0])))
