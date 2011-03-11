"""
Generic web-site grabber

Many oblique services wound up being something like "Go to this URL, and
find this particular spot in the page it returns, and send that back
unformatted."  So it made sense to make one that subsumes all of them and
can be configured to do essentially the same thing by the url used.

So this script takes a URL and an xpath selector, goes and fetches the
page, parses it (with the help of html5lib) and selects the node(s)
specified by the xpath, and returns the first 200(?) characters of the text
under them.

To use it, specify a url on the oblique services wiki page that looks like:

xx http://tumbolia.appspot.com/general//http://www.blahblahblah.org/foo/bar/baz%3fquux=${args}||//x:div[@class='answer']

(I'm assuming the service is run off tumbolia.appspot.com)

This would fetch http://www.blahblahblah.org/foo/bar/baz?quux=<...> where 
that last bit is replaced by the arguments from the query line, and then 
it would search for a <div> element of class "answer" and return the text 
under it.

So basically, after the /general/ comes the URL of wherever you're going,
possibly including the arguments and whatever, followed by the string "||",
which is used as a separator (you're on your own if you need to use it in
your xpath).  Then comes the xpath selector of the the spot in the page
that you're looking for.

A few "gotchas" apply:

 1. Not sure how much of the URL you need to escape with %xx.  You probably 
    should escape spaces (using %20).  You *definitely* need to escape the
    question mark, which is very likely to be in your url and will cut things
    off if you forget to escape it, using %3f.  That's probably the most
    important; you may want to escape [], quotes, &, etc.  But it is crucial
    that you use %3f in place of ?.

 2. For annoying reasons, you need to prefix the names of any elements in
    your xpath selector with "x:", as above.  So you can't say 
    "/body/div[@class='header']/p[3]", but you need to say
    "/x:body/x:div[@class='header']/x:p[3]".  It may work for some pages if
    you forget to do this, but don't count on it.  Sorry, this one is really
    strange.
"""
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
    it=con.find(xpth+"//text()", pars.documentElement)
    if not it:
        return "ENOTFOUND"
    stuff=reduce((lambda x,y: x+y), map((lambda x: x.data), it))
    stuff=stuff.replace("\n"," ").strip()
    return stuff[:200]

class Main(base.RequestHandler):

    def get(self,*args):
        stuff=os.environ['PATH_INFO']
        a=stuff.split('/',2)
        stuff=a[2]
        try:
            (uri, xpth)=stuff.rsplit('||',1)
        except ValueError:
            return self.ok("Bad service format.")
        return self.ok(do_generic_parse(uri, xpth))
