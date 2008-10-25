import logging
import urllib
import re

from google.appengine import api

import base
from contrib import feedparser

log = logging.getLogger(__name__)

URI="http://issues.apache.org/jira/si/jira.issueviews:issue-xml"

class Main(base.RequestHandler):
    projre = re.compile("^\w+-\d+$")
    numre = re.compile("^\d+$")

    def get(self, *args):
        logging.basicConfig(level=logging.DEBUG)
        log.debug("HI!")
        tag = args[-1] or ""
        if self.projre.match(tag):
            tag = tag.upper()
        elif self.numre.match(tag):
            tag = "COUCHDB-%s" % tag
        else:
            return self.ok("Unrecognized ticket id: %r" % tag)
        url = '/'.join([URI, tag, "%s.xml" % tag])
        resp = api.urlfetch.fetch(url)
        if resp.status_code != 200:
            return self.ok("Failed to find ticket: %r\n(%s) %s" % (tag, resp.status_code, url))
        else:
            d = feedparser.parse(resp.content)
            item = d["items"][0]
            return self.ok("%s [%s] %s" % (item["link"], item["type"], item["content"][0]["value"]))
