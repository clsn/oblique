import re
import urllib

from google.appengine import api

import base

YOUTUBE_API_URI = "http://www.youtube.com/get_video.php"
TINYURL_API_URI = "http://tinyurl.com/api-create.php"

class Main(base.RequestHandler):

    def get(self, *args, **kwargs):
        uri = args[1] or ""
        if not uri:
            return self.ok("Please provide a video URI.")
        uri = urllib.unquote(uri)
        html = urllib.urlopen(uri).read()
        try:
            video_id, t = re.findall("&video_id=([^&]+).*&t=([^&]+)", html)[0]
        except:
            return self.ok("Unable to extract video information.")
        youtube_query = urllib.urlencode({
            "video_id": urllib.unquote(video_id), "t": urllib.unquote(t)})
        youtube_uri = YOUTUBE_API_URI + "?" + youtube_query
        tinyurl_query = urllib.urlencode({"url": youtube_uri})
        tinyurl_uri = TINYURL_API_URI + "?" + tinyurl_query
        self.ok(urllib.urlopen(tinyurl_uri).read())
