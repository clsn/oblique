import BeautifulSoup
import fnmatch
import urllib

from google.appengine import api

import base

class Main(base.RequestHandler):

    def get(self, *args):
        args = args[1] or ""
        args = urllib.unquote(args).lower()
        args = args.split(" ")
        if len(args) > 0:
            command = args[0]
        else:
            command = None
        if len(args) > 1:
            query = " ".join(args[1:])
        else:
            query = None
        if not command:
            return self.ok("Please specify a command: find show gen")
        if not command in ["find", "show", "gen"]:
            return self.ok("Invalid command.")
        if command in ["find", "show"] and not query:
            return self.ok("Please specify a query.")
        if command == "find":
            if "*" not in query:
                query = "*%s*" % query
            matches = []
            for name in file("gazetteer/output/unique.txt").readlines():
                name = name.strip()
                if fnmatch.fnmatch(name.lower(), query):
                    matches.append(name)
                if len(matches) > 19:
                    break
            if matches:
                return self.ok(", ".join(matches))
            else:
                return self.ok("No matches.")
        if command == "show":
            return self.ok("Patches welcome!")
        if command == "gen":
            return self.ok("Patches welcome!")
