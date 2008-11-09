import wsgiref.handlers

from google.appengine.ext import webapp

import base
import christmas
import identica
import lastfm
import fact
import steps
import soccer
import stupid
import ticket
import unicode
import internet
import vary
import googlesets
import search

uris = [
  ("^/$", base.Index),
  ("^/christmas(/.*?)?", christmas.Main),
  ("^/identica(/(.*?))?(/(.*?))?/?", identica.Main),
  ("^/lastfm(/(.*?))?(/(.*?))?/?", lastfm.Main),
  ("^/fact(/(.*?))?/?", fact.Main),
  ("^/soccer(/(.*?))?/?", soccer.Main),
  ("^/steps(/(.*?))?/?", steps.Main),
  ("^/stupid(/(.*?))?/?", stupid.Main),
  ("^/ticket(/(.*?))?(/(.*?))?/?", ticket.Main),
  ("^/internet(/(.*?))?/?", internet.Main),
  ("^/unicode(/(.*?))?/?", unicode.Main),
  ("^/vary(/(.*?))?/?", vary.Main),
  ("^/sets(/(.*?))?/?", googlesets.Main),
  ("^/search(/(.*?))?(/(.*?))?/?", search.Main),
  ("^/.*$", base.NotFound)
]

def main():
  wsgiref.handlers.CGIHandler().run(webapp.WSGIApplication(uris, debug=True))

if __name__ == "__main__":
  main()
