from google.appengine.api import urlfetch
from google.appengine.ext import webapp

from xml.dom.minidom import parseString
from xml.parsers.expat import ExpatError


class IdenticaService(webapp.RequestHandler):

  def get(self, user):
    try:
      f = urlfetch.fetch('http://identi.ca/%s/rss' % user)
      xml = f.content
      doc = parseString(xml)
      
    except:
      self.response.out.write("ERROR")
      return
    
    try:
      text = doc.getElementsByTagName('title')[2].firstChild.nodeValue
    except:
      self.response.out.write("%s has zero posts" % user)
      return
    
    self.response.out.write(text)
