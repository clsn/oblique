import urllib

from google.appengine import api

import base
from contrib import feedparser

URI="http://issues.apache.org/jira/si/jira.issueviews:issue-xml"

class Main(base.RequestHandler):

    def get(self, *args):
        if not args[1] or not args[3]:
            return self.ok("Invalid ticket path: %s" % self.request.path)
        project = urllib.unquote(args[1]).lstrip("#").upper()
        tag = "%s-%s" % (project, args[3])
        url = '/'.join([URI, tag, "%s.xml" % tag])
        resp = api.urlfetch.fetch(url)
        if resp.status_code != 200:
            return self.ok("Failed to find ticket: %r\n(%s) %s" % (tag, resp.status_code, url))
        else:
            d = feedparser.parse(resp.content)
            item = d["items"][0]
            ret = "[%s] %s" % (item["type"], item["content"][0]["value"])
            link = item["link"]
            return self.ok("%s %s" % (ret[:350 - len(link) - 1], link))
