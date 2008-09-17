from google.appengine.ext import webapp

URI = "http://code.google.com/p/phenny-ws/"

def collapse(string):
    return " ".join(string.split())

class RequestHandler(webapp.RequestHandler):

    def ok(self, message):
        self.response.headers['Content-Type'] = "text/plain"
        self.response.out.write(message + "\n")

class Index(RequestHandler):

    def get(self):
        return self.ok("Phenny Web Services, see %s for details." % URI)

class NotFound(RequestHandler):

    def get(self):
        return self.ok("Service not found, see %s for details." % URI)

