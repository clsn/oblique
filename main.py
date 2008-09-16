import wsgiref.handlers
from google.appengine.ext import webapp

import identica

def main():
  application = webapp.WSGIApplication([('^/identi.ca/(.+)/?$', identica.IdenticaService)], debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
