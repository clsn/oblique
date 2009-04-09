import wsgiref.handlers

from google.appengine.ext import webapp

import base
import mirror
import identica
import lastfm
import fact
import steps
import soccer
import stupid
import ticket
import unicode
import entity
import internet
import vary
import googlesets
import search
import connect
import isbn
import dwim
import whois
import speak

uris = [
  ("^/$", base.Index),
  ("^/mirror(/.*?)?", mirror.Main),
  ("^/identica(/(.*?))?(/(.*?))?/?", identica.Main),
  ("^/lastfm(/(.*?))?(/(.*?))?/?", lastfm.Main),
  ("^/fact(/(.*?))?/?", fact.Main),
  ("^/soccer(/(.*?))?/?", soccer.Main),
  ("^/steps(/(.*?))?/?", steps.Main),
  ("^/stupid(/(.*?))?/?", stupid.Main),
  ("^/ticket(/(.*?))?(/(.*?))?/?", ticket.Main),
  ("^/internet(/(.*?))?/?", internet.Main),
  ("^/unicode(/(.*?))?/?", unicode.Main),
  ("^/entity(/(.*?))?/?", entity.Main),
  ("^/vary(/(.*?))?/?", vary.Main),
  ("^/sets(/(.*?))?/?", googlesets.Main),
  ("^/search(/(.*?))?/?", search.Main),
  ("^/connect(/(.*?))?/?", connect.Main),
  ("^/isbn(/(.*))?/?", isbn.Main),
  ("^/dwim(/(.*))?/?", dwim.Main),
  ("^/whois(/(.*))?/?", whois.Main),
  ("^/speak(/(.*))?/?", speak.Main),
  ("^/.*$", base.NotFound)
]

def main():
  wsgiref.handlers.CGIHandler().run(webapp.WSGIApplication(uris, debug=True))

if __name__ == "__main__":
  main()
