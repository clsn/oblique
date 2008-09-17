import wsgiref.handlers

from google.appengine.ext import webapp

import base
import identica
import lastfm

uris = [
  ('^/$', base.Index),
  ('^/identica(/(.*?))?(/(.*?))?/?', identica.Main),
  ('^/lastfm(/(.*?))?(/(.*?))?/?', lastfm.Main),
  ('^/.*$', base.NotFound)
]

def main():
  wsgiref.handlers.CGIHandler().run(webapp.WSGIApplication(uris, debug=True))

if __name__ == "__main__":
  main()
