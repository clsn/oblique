import random

import base

class Main(base.RequestHandler):

    responses = [
        "Sure thing, please give me a second.",
        "Processing now, please wait a few minutes.",
        "Of course, please check back later.",
        "Okay, working on it now.",
        "No problem, please monitor the channel for updates."]

    def get(self, *args):
        request = args[1] or ""
        if not request:
            return self.ok("Oh come on, at least give me a clue!")
        return self.ok(self.responses[random.randint(0, 4)])
