from __future__ import unicode_literals
import musicbrainzngs
import sys
import time
#import numpy as np
import json
#import urllib2
import csv

#artist='paddy and the rats'
#artist ='ac/dc'
#artist = 'sean paul'
#track='Hells+Bells'
#tag='rock'
#album='hymns for bastards'
#album='Back in Black'
#album = 'she doesn\'t mind'
country='GB'

datelist = []

# User-Agent string is needed for every request: App name, apps version number,
# contact-url or -email. This is an example:
musicbrainzngs.set_useragent(
    "python-musicbrainzngs-example",
    "0.1",
    "https://github.com/alastair/python-musicbrainzngs/",
)

def iterate_over_file(csv_in):
    count = 0
    total = 0
    for rownum,row in enumerate(csv_in):
        if (len(row)<=3) or (rownum==0): #line too short or first line
            continue
        artist=row[1]
        album=row[2]
        search_tags(artist,album)
        search_releases(artist, album)
        count = count + 1
        total = total + 1
        if count == 20:
            time.sleep(1)
            count = 0
        if total == 20:
            break

def read_csv_file():
    csv_infile = open('data.csv', "r")
    #csv_infile = io.open("data_less.csv", "r", encoding="utf-8")
    csv_in = csv.reader(csv_infile)
    return csv_in

def read_genrenames_file():
    infile = open('Genres.txt', "r")
    txt_in = csv.reader(infile)
    return txt_in
    

def compare_name(first, second):
    f = first.lower()
    s = second.lower()
    f_in_s = s.find(f)
    s_in_f = f.find(s)
    if f_in_s > 0 or s_in_f > 0 or f == s:
        return 1
    else:
        return 0

def show_release_details(rel, artistname, albumname):
    """Print some details about a release dictionary to stdout.
    """
    # "artist-credit-phrase" is a flat string of the credited artists
    # joined with " + " or whatever is given by the server.
    # You can also work with the "artist-credit" list manually.
    print("{}, by {}".format(rel['title'], rel["artist-credit-phrase"]))
    print albumname.lower()
    print artistname.lower()
    #if (rel['artist-credit-phrase'].lower() == artistname.lower() and
    if compare_name(rel['artist-credit-phrase'], artistname) == 1 and compare_name(rel['title'], albumname) == 1:
        #rel['title'].lower() == albumname.lower()):
        if 'date' in rel:
            print("Released {}".format(rel['date']))
            datelist.append(rel['date'])
        #print("MusicBrainz ID: {}".format(rel['id']))
    #print(json.dumps(result2, indent=4))

def show_recording_details(rel):
    print("{}, by {}".format(rel['title'], rel["artist-credit-phrase"]))
    if 'date' in rel:
        print("Recorded {} ({})".format(rel['date'], rel['status']))
    #print(rel)

def show_first_release_date():
    datelist.sort()
    if len(datelist) != 0:
        print "first release date: ", datelist[0]
        del datelist[:]

def show_tags(rel):
    print(json.dumps(rel, indent=4))

def show_taglist(result,artistname):
    if not result['release-list']:
        sys.exit("no release found")
    for (idx, release) in enumerate(result['release-list']):
        if not 'artist-credit-phrase' in release:
            print("No artist credit name given");
        else:
            #print("Artist: ", release['artist-credit-phrase'])

            if (release['artist-credit-phrase'].lower() == artistname.lower()):
                if 'tag-list' in release:
                    for tag in release['tag-list']:
                        print ("Found tag", tag)

def search_releases(artistname, albumname):
    # Keyword arguments to the "search_*" functions limit keywords to
    # specific fields. The "limit" keyword argument is special (like as
    # "offset", not shown here) and specifies the number of results to
    # return.
    result = musicbrainzngs.search_releases(artist=artistname, release=albumname,
                                            limit=10)
    # On success, result is a dictionary with a single key:
    # "release-list", which is a list of dictionaries.
    if not result['release-list']:
        sys.exit("no release found")
    for (idx, release) in enumerate(result['release-list']):
        print("match #{}:".format(idx+1))
        show_release_details(release, artistname, albumname)
    show_first_release_date()

def search_artist():
    result = musicbrainzngs.search_artists(artist=artist, type="group", country=country)
    for artst in result['artist-list']:
        print(u"{id}:{name}".format(id=artst['id'], name=artst["name"]))

        
def search_recordings():
    result = musicbrainzngs.search_recordings(artist=artist, release=album,
                                            limit=5)
    show_tags(result)

def search_tags(artistname, albumname):
    result = musicbrainzngs.search_releases(artist=artistname, release=albumname,
                                            limit=50)
    show_taglist(result,artistname)

def filter_genre_results(tag):
    data_in = read_genrenames_file()

    

#main
#search_tags(artist, album)
csv = read_csv_file()
iterate_over_file(csv)

