import xml.dom.minidom
import html5lib
import xml
import xpath
import csv
import re
import StringIO
import urllib
import os

from google.appengine import api

import base

def gettext(nod):
    if not nod:
        return ''
    elif isinstance(nod, xml.dom.minidom.Text):
        return nod.data
    elif isinstance(nod, xml.dom.minidom.Element):
        rv=''
        for n in nod.childNodes:
            rv+=gettext(n)
        return rv
    return "?????"

def do_generic_parse(url, xpth):
    url=url.replace(' ','%20')
    thepage=api.urlfetch.fetch(url).content
    fp=StringIO.StringIO(thepage)
    try:
        pars=html5lib.parse(fp, treebuilder="dom")
    except Exception, e:
        return "something failed: %s (%s)."%(str(e),str(type(e)))
    if not pars:
        return "Parsing failed for some reason"
    con=xpath.XPathContext()
    con.namespaces["x"]="http://www.w3.org/1999/xhtml"
    it=con.find(xpth, pars.documentElement)
    if not it:
        return "ENOTFOUND"
    stuff=gettext(it[0]).replace("\n"," ").strip()
    return stuff[:200]

class Main(base.RequestHandler):

    def get(self,*args):
        stuff=os.environ['PATH_INFO']
        a=stuff.split('/',2)
        stuff=a[2]
        # stuff=urllib.unquote(args[1])
        try:
            (uri, xpth)=stuff.rsplit('||',1)
        except ValueError:
            return self.ok("Bad service format.")
        return self.ok(do_generic_parse(uri, xpth))
