from google.appengine.ext import webapp

URI = "http://github.com/nslater/oblique"

def collapse(string):
    return " ".join(string.split())

class RequestHandler(webapp.RequestHandler):

    def ok(self, message):
        self.response.headers["Content-Type"] = "text/plain"
        self.response.out.write(message.rstrip() + "\n")

class Index(RequestHandler):

    def get(self):
        return self.ok("See %s for details." % URI)

class NotFound(RequestHandler):

    def get(self):
        req = self.request.path
        return self.ok("Service not found." % (req, URI))
