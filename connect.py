import urllib
import StringIO
import csv

from google.appengine import api

import base
from contrib import BeautifulSoup
import re

baseuri="http://oracleofbacon.org/cgi-bin/movielinks"

class Main(base.RequestHandler):

    def getit(self, actor1, actor2):
        dct={ 'game': 0,                # What other options?
              'firstname': actor1,
              'secondname': actor2,
              'using': 1,
              'start_year': 1850,
              'end_year': 2050,
              'dir': 0,
              'use_genres': 0,          # ???
              }
        query=urllib.urlencode(dct)
        try:
            fetch=api.urlfetch.fetch(baseuri+'?'+query)
            html=fetch.content
        except Exception:
            return self.ok("Error fetching results")
        try:
            self.tree = BeautifulSoup.BeautifulSoup(html)

            actr=self.tree.find('span', {'class':'actor'})
            rv=[]
            # alternation is actor/movie/actor/movie/actor... one MORE actor than there
            # are movies!
            while actr:
                # Actor's name is in <a> elt inside actr
                actorname=actr.find('a')
                actorname=str(actorname.string)
                movie=actr.findNext('span', {'class' : 'film'})
                if not movie:
                    moviename=''
                    actr=None
                else:
                    moviename=str(movie.find('a').string)
                    actr=movie.findNext('span', {'class' : 'actor'})
                rv.append((actorname, moviename))
            message=''
            for x in rv:
                message+="%s(%s) -> "%x
            if len(message)>3:
                message=message[:-3]
        except:
            message="Error parsing results."
        return message

    def get(self,*args):
        try:
            query=base.collapse(urllib.unquote(args[1]))
            query=StringIO.StringIO(query)
            words=csv.reader(query, delimiter=" ").next()
            actor1=words[1]
            actor2=words[0]
        except Exception:
            return self.ok("Please provide exactly two actor names.")
        message=self.getit(actor1, actor2)
        if not message:
            # Try this?
            u=self.tree.find('i')
            name=str(u.string)
            [f, s]=name.split(' ',1)
            if actor1 == name:
                actor1 = "%s, %s (I)"%(s,f)
            else:
                actor2 = "%s, %s (I)"%(s,f)
            message=self.getit(actor1, actor2)
            if not message:
                # FAIL
                message="One or both of those actors was not unique in the database.  We even tried (%s)"%str((actor1,actor2))
            else:
                message=("((Tried (%s))) "%str((actor1, actor2)))+message
        return self.ok(message)
