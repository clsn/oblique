Oblique
=======

A collection of tiny web services, usable by anyone.

The [Phenny](http://inamidst.com/phenny/) IRC bot lets you use all of the services listed on the [wiki](http://wiki.github.com/nslater/oblique/) with the `oblique` command.

If `nslater` wanted to use the LastFM service he might do:

    <nslater> .o lastfm USERNAME
    <phenny> Now playing Track by Artist from the album Album - http://www.last.fm/music/Artist/_/Track

Since USERNAME defaults to IRC nick he can also do:

    <nslater> .o lastfm
    <phenny> Now playing Track by Artist from the album Album - http://www.last.fm/music/Artist/_/Track

You can configure Phenny to use your own custom services by adding the following to your configuration:

    services = "http://example.org/your-service-definitions"

After adding a new service you must refresh Phenny:

    <nslater> .o refresh
    <phenny> nslater: Okay, found 20 services.

Phenny will now be able to call any of the services listed by using the `oblique` command:

    <nslater> .o name
    <phenny> results

Service urls may include the following variables that will automatically be replaced:

 * @${args}@ - Arguments included after the command name
 * @${sender}@ - If sent from a channel, the channel name. If sent via privmsg the same as @${nick}@
 * @${nick}@ - Nick of message sender
