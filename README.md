Phenny Web Services
===================

A collection of Web services for the [Phenny](http://inamidst.com/phenny/) IRC bot:

> Phenny is a popular IRC bot written in Python. She runs on the Freenode IRC server amongst others, and has the usual sundry facilities that one expects from an IRC bot, such as Wikipedia and dictionary lookups. She is modularly extensible, and can reload modules on the fly.

Phenny is pre-configured to use all of the services listed here with the `oblique` command.

If `nslater` wanted to use the LastFM service he might do:

    <nslater> .o lastfm USERNAME
    <phenny> Now playing Track by Artist from the album Album - http://www.last.fm/music/Artist/_/Track

Since USERNAME defaults to IRC nick he can also do:

    <nslater> .o lastfm
    <phenny> Now playing Track by Artist from the album Album - http://www.last.fm/music/Artist/_/Track

You can configure Phenny to use your own custom services by adding the following to your configuration:

    services = "http://example.org/your-service-definitions"

Make sure to follow the same style as ServiceDefinitions when creating this page.
