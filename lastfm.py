import urllib
from xml.etree import ElementTree

from google.appengine import api

import base

API_URI = "http://ws.audioscrobbler.com/2.0/"
API_KEY = "127e282d134878fc81b8426882de03e6"

override = {
    "arnia": "jgeldart",
    "nslater": "noahslater",
    "tav": "asktav"
}

class Main(base.RequestHandler):

    def get(self, *args):
        user = args[1] or ""
        if args[3]:
            user = args[3]
        if not user:
            return self.ok("Please provide a username.")
        user = override.get(user.lower(), user)
        query = urllib.urlencode(
            {"method": "user.getrecenttracks", "api_key": API_KEY, "user": user})
        uri = API_URI + "?" + query
        try:
            tree = ElementTree.XML(api.urlfetch.fetch(uri).content)
        except Exception, error:
            return self.ok("No user details found.")
        track = tree.find(".//track")
        if not track:
            return self.ok("No tracks found.")
        if track.get("nowplaying"):
            status = "Now playing "
        else:
            status = "Last played "
        name = base.collapse(track.find(".//name").text)
        artist = base.collapse(track.find(".//artist").text)
        album = base.collapse(track.find(".//album").text)
        url = base.collapse(track.find(".//url").text)
        message = ""
        if name:
            message = status + name
        if artist:
            message += " by %s" % artist
        if album:
            message += " from the album %s" % album
        if url:
            message += " - %s" % url
        if not message:
            return self.ok("No track information found.")
        return self.ok(message.encode("utf8"))
