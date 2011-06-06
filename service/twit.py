from google.appengine import api

import base
import simplejson as json
import urllib
import re

def format(bits):
    format = "%(text)s - http://twitter.com/%(username)s/%(id)s"
    msg = format % {
        "id": bits["id"],
        "username": bits["user"]["screen_name"],
        "text": bits["text"],
    }
    return msg

def fetchbyID(term):
    resp=api.urlfetch.fetch('http://api.twitter.com/statuses/show/'+ \
                                term + '.json').content
    bits=json.loads(resp)
    if bits.has_key('error'):
        ans=bits['error']
    elif bits.has_key('text'):
        ans=format(bits)
    else:
        ans="could not fetch tweet by ID"
    return re.sub(r'\s+', ' ', ans)


class Main(base.RequestHandler):

    def get(self,*args):
        # Args is just a string...
        # well, args[1] anyway
        arg=None
        try:
            arg=args[1]
        except IndexError:
            pass
        if not arg:
            return self.ok("You must supply a username or something")
        params=urllib.unquote(arg).strip().split()      # split on whitespace.
        if len(params)==1:
            # Only one parameter.  By default a username.  Also allow
            # a twitter URL (distinguished by http:// of course) or an id
            # number
            term=params[0]
            ans=None
            if term.startswith('http://'):
                # http://twitter.com/username/status/46611258765606912
                m=re.match(r'http://(?:www\.)?twitter\.com/\w*/status/(\d+)',
                           term)
                if not m:
                    return self.ok("Could not parse twitter url")
                return self.ok(fetchbyID(m.group(1)))
            if term.isdigit():
                # This enough to tell if it's a status id#?  Is it possible
                # to have a username that's all numbers?
                return self.ok(fetchbyID(term))
            else:
                # Otherwise, a user.
                # Should I check if its all alnum or something?  Probably.
                if not term.isalnum():
                    return self.ok("%s did not look like a username"%term)
                resp=api.urlfetch.fetch('http://api.twitter.com/users/show/'+ \
                                      term + '.json').content
                bits=json.loads(resp)
                if bits.has_key('error'):
                    ans=bits['error']
                elif bits.has_key('status') and \
                        bits['status'].has_key('text'):
                    ans=format(bits['status'])
                else:
                    ans=str(bits['status'])
            if not ans:
                ans='???'
            return self.ok(re.sub('\s+',' ',ans))
        elif len(params)==2:
            # two params means user and status id, which is the same as
            # just status id.
            return self.ok(fetchbyID(params[1]))
        else:
            return self.ok("??")
