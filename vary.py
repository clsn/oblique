#!/usr/bin/env python

import os
import re
import urllib2

def fetch(uri):
    if not uri:
        return "Please provide a URI."
    if not uri.startswith("http://"):
        uri = "http://" + uri
    request = urllib2.Request(uri, None, {"Negotiate": "trans", "Accept": ""})
    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError, error:
        if error.code not in (300, 406):
            return "Response was %d, expected 300 or 406." % error.code
        alternates = error.headers.dict.get("alternates")
        if not alternates:
            return "Resource does not support transparent content negotiation."
        alternates =  re.compile("\"([^\"]+)\"").findall(alternates)
        if not alternates:
            return "Resource negotiates but no variants found."
        if len(alternates) == 1:
            return "Single variant: %s" % alternates[0]
        else:
            return "Multiple variants: %s" % ", ".join(alternates)
    except Exception, error:
        return "Unable to dereference URI."
    vary = response.headers.dict.get("vary")
    if vary:
        return "Resource claims to vary on: %s" % vary
    else:
        return "Resource does not vary."

def main():
    print "Content-Type: text/plain; charset=utf-8"
    print
    print fetch(os.environ.get("QUERY_STRING"))

if __name__ == "__main__":
    main()
