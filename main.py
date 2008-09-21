import wsgiref.handlers

from google.appengine.ext import webapp

import base
import identica
import lastfm
import fact
import steps
import soccer
import stupid

uris = [
  ("^/$", base.Index),
  ("^/identica(/(.*?))?(/(.*?))?/?", identica.Main),
  ("^/lastfm(/(.*?))?(/(.*?))?/?", lastfm.Main),
  ("^/fact(/(.*?))?/?", fact.Main),
  ("^/soccer(/(.*?))?/?", soccer.Main),
  ("^/steps(/(.*?))?/?", steps.Main),
  ("^/stupid(/(.*?))?/?", stupid.Main),
  ("^/.*$", base.NotFound)
]

def main():
  wsgiref.handlers.CGIHandler().run(webapp.WSGIApplication(uris, debug=True))

if __name__ == "__main__":
  main()
