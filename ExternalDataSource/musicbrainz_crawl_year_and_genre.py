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
        print (search_tags(artist,album))
        print (search_releases(artist, album))
        count = count + 1
        total = total + 1
        if count == 20:
            time.sleep(1)
            count = 0
        if total == 20:
            break

def iterate_over_textfile(genre):
    with open("Genres.txt") as f:
        genres = f.readlines()
        genres = [x.strip().lower() for x in genres] #remove whitespaces and linebreakes and make lower case
        for name in genres:
            if name == genre:
                return True
    return False

# read csv file
def read_csv_file():
    csv_infile = open('data.csv', "r")
    csv_in = csv.reader(csv_infile)
    return csv_in

# compare the names (equal or substring)
def compare_name(first, second):
    f = first.lower()
    s = second.lower()
    f_in_s = s.find(f)
    s_in_f = f.find(s)
    if f_in_s > 0 or s_in_f > 0 or f == s:
        return True
    else:
        return False

# filter the search result for the release dates
def show_release_details(rel, artistname, albumname):
    if compare_name(rel['artist-credit-phrase'], artistname) and compare_name(rel['title'], albumname):
        if 'date' in rel:
            datelist.append(rel['date'])


# filter the date result list for the first release date
def show_first_release_date():
    datelist.sort()
    if len(datelist) != 0:
        erg = datelist[0]
        del datelist[:]
        return erg

def show_tags(rel):
    print(json.dumps(rel, indent=4))

# filter the search result for tags
def show_taglist(result,artistname):
    genres = []
    if not result['release-list']:
        return [] #no list was found
    for (idx, release) in enumerate(result['release-list']):
        if not 'artist-credit-phrase' in release:
            print("No artist credit name given");
        else:
            if (release['artist-credit-phrase'].lower() == artistname.lower()):
                if 'tag-list' in release:
                    for tag in release['tag-list']:
                        genres.append(tag['name'])
    return genres

# search for releases and return the first release date (by artist and album)
def search_releases(artistname, albumname):
    result = musicbrainzngs.search_releases(artist=artistname, release=albumname,
                                            limit=10)
    if not result['release-list']:
        sys.exit("no release found")
    for (idx, release) in enumerate(result['release-list']):
        show_release_details(release, artistname, albumname)
    return show_first_release_date()

# search for releases and return a list of genres (by artist)
def search_tags(artistname, albumname):
    result = musicbrainzngs.search_releases(artist=artistname, release=albumname,
                                            limit=50)
    return show_taglist(result,artistname)

# delete doubles
def filter_genre_results(taglist):
    return sorted(set(taglist), key=taglist.index)
