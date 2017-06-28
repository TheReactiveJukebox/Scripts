import numpy as np
import json
import urllib2

artist='AC/DC'
track='Hells+Bells'

#similar artists to given artist
#result=json.load(urllib2.urlopen("http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist=cher&api_key=a8b40052edf6a8ce494429b0b3b10f91&format=json"))
#print([x['name'].encode('UTF-8') for x in result['similarartists']['artist'] ])

#tags to given track
result=json.load(urllib2.urlopen("http://ws.audioscrobbler.com/2.0/?method=track.getTags&api_key=a8b40052edf6a8ce494429b0b3b10f91&artist="+artist+"&track="+track+"&user=RJ&format=json"))
print([x['name'].encode('UTF-8') for x in result['tags']['tag'] ])
