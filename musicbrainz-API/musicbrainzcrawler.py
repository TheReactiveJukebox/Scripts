from __future__ import unicode_literals

import json
import sys

import musicbrainzngs

artist = 'AC/DC'
# track='Hells+Bells'
# tag='rock'
album = 'Back in Black'

# User-Agent string is needed for every request: App name, apps version number,
# contact-url or -email. This is an example:
musicbrainzngs.set_useragent(
    "python-musicbrainzngs-example",
    "0.1",
    "https://github.com/alastair/python-musicbrainzngs/",
)


def show_release_details(rel):
    """Print some details about a release dictionary to stdout.
    """
    # "artist-credit-phrase" is a flat string of the credited artists
    # joined with " + " or whatever is given by the server.
    # You can also work with the "artist-credit" list manually.
    print("{}, by {}".format(rel['title'], rel["artist-credit-phrase"]))
    if 'date' in rel:
        print("Released {} ({})".format(rel['date'], rel['status']))
    print("MusicBrainz ID: {}".format(rel['id']))


def search():
    # Keyword arguments to the "search_*" functions limit keywords to
    # specific fields. The "limit" keyword argument is special (like as
    # "offset", not shown here) and specifies the number of results to
    # return.
    result = musicbrainzngs.search_releases(artist=artist, release=album,
                                            limit=5)

    # On success, result is a dictionary with a single key:
    # "release-list", which is a list of dictionaries.
    if not result['release-list']:
        sys.exit("no release found")
    for (idx, release) in enumerate(result['release-list']):
        print("match #{}:".format(idx + 1))
        show_release_details(release)
    print(' ')
    print(json.dumps(result, indent=4))


search()
