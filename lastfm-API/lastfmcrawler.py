#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import csv
import json
import time
# import musicbrainzngs
import urllib
import urllib2

artist = 'AC/DC'
track = 'Hells+Bells'

# similar artists to given artist
# result=json.load(urllib2.urlopen("http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist=cher&api_key=a8b40052edf6a8ce494429b0b3b10f91&format=json"))
# print([x['name'].encode('UTF-8') for x in result['similarartists']['artist'] ])

# tags to given track
# result=json.load(urllib2.urlopen("http://ws.audioscrobbler.com/2.0/?#method=track.getTags&api_key=a8b40052edf6a8ce494429b0b3b10f91&artist="+artist+"&track="+track+"&user=RJ&format=json"))
# print([x['name'].encode('UTF-8') for x in result['tags']['tag'] ])


# read genres
with open("genres.txt") as f:
    genres = f.readlines()
    genres = [x.strip().lower() for x in genres]  # remove whitespaces and linebreakes and make lower case

out = open("data_out.csv", "w")
csv_out = csv.writer(out, delimiter=',')

# csv_infile = open('beispiel.csv', "r")
# csv_in = csv.reader(csv_infile, delimiter=';')

csv_infile = open('data.csv', "r")
# csv_infile = io.open("data_less.csv", "r", encoding="utf-8")
csv_in = csv.reader(csv_infile, delimiter=',')

genrecount = {}

timestart = time.time()  # current time in seconds

counter = 0  # how many songs are already crawled
# notfound_lfm_xxx counts up if no information could be crawled
notfound_lfm_track = 0
notfound_lfm_playcount = 0
notfound_lfm_listeners = 0
notfound_lfm_trackmbid = 0
notfound_lfm_artistmbid = 0
notfound_lfm_albummbid = 0
notfound_lfm_album = 0
notfound_lfm_albumcover = 0
notfound_lfm_tags = 0

for rownum, row in enumerate(csv_in):

    if (len(row) <= 3):  # line too short
        continue

    if (rownum == 0):
        csv_out.writerow(('title', 'artist', 'album', 'songHash', 'length', 'published', 'trackmbid', 'artistmbid',
                          'albummbid', 'playcount', 'listeners', 'albumcover', 'genres'))
        continue  # next row

    title = row[0]
    artist = row[1]
    album = row[2]
    songHash = row[3]
    length = row[4]
    print(str(rownum) + " t=" + str(round(time.time() - timestart)) + ": " + artist + " - " + title)

    apiParams = '&api_key=a8b40052edf6a8ce494429b0b3b10f91&artist=%s&track=%s&user=RJ&format=json' % (
    urllib.quote(artist), urllib.quote(title))
    infoURL = 'http://ws.audioscrobbler.com/2.0/?method=track.getInfo' + apiParams
    result_info = json.load(urllib2.urlopen(infoURL))

    tagURL = 'http://ws.audioscrobbler.com/2.0/?method=track.getTags' + apiParams
    result_tags = json.load(urllib2.urlopen(tagURL))

    # print([x['name'].encode('UTF-8') for x in result['tags']['tag'] ])



    counter += 1

    if 'name' in result_info['track']:
        lfm_track = result_info['track']['name'].encode('UTF-8')
    else:
        lfm_track = ''
        notfound_lfm_track += 1

    if 'playcount' in result_info['track']:
        lfm_playcount = result_info['track']['playcount'].encode('UTF-8')
    else:
        lfm_playcount = '0'
        notfound_lfm_playcount += 1

    if 'listeners' in result_info['track']:
        lfm_listeners = result_info['track']['listeners'].encode('UTF-8')
    else:
        lfm_listeners = '0'
        notfound_lfm_listeners += 1

    if 'mbid' in result_info['track']:
        lfm_trackmbid = result_info['track']['mbid'].encode('UTF-8')
    else:
        lfm_trackmbid = ''
        notfound_lfm_trackmbid += 1

    if 'artist' in result_info['track']:
        if 'mbid' in result_info['track']['artist']:
            lfm_artistmbid = result_info['track']['artist']['mbid'].encode('UTF-8')
        else:
            lfm_artistmbid = ''
            notfound_lfm_artistmbid += 1
    else:
        lfm_artistmbid = ''
        notfound_lfm_artistmbid += 1

    if 'album' in result_info['track']:
        if 'mbid' in result_info['track']['album']:
            lfm_albummbid = result_info['track']['album']['mbid'].encode('UTF-8')
        else:
            lfm_albummbid = ''
            notfound_lfm_albummbid += 1
    else:
        lfm_albummbid = ''
        notfound_lfm_albummbid += 1

    if 'album' in result_info['track']:
        if 'title' in result_info['track']['album']:
            lfm_album = result_info['track']['album']['title'].encode('UTF-8')
        else:
            lfm_album = ''
            notfound_lfm_album += 1
    else:
        lfm_album = ''
        notfound_lfm_album += 1

    if 'album' in result_info['track']:
        if 'image' in result_info['track']['album']:
            lfm_albumcover = result_info['track']['album']['image'][-1]['#text'].encode('UTF-8')
        else:
            lfm_albumcover = ''
            notfound_lfm_albumcover += 1
    else:
        lfm_albumcover = ''
        notfound_lfm_albumcover += 1

    # old without check if available:
    # lfm_track=result_info['track']['name'].encode('UTF-8')
    # lfm_playcount=result_info['track']['playcount'].encode('UTF-8')
    # lfm_listeners=result_info['track']['listeners'].encode('UTF-8')
    # lfm_trackmbid=result_info['track']['mbid'].encode('UTF-8')
    # lfm_artistmbid=result_info['track']['artist']['mbid'].encode('UTF-8')
    # lfm_albummbid=result_info['track']['album']['mbid'].encode('UTF-8')
    # lfm_album=result_info['track']['album']['title'].encode('UTF-8')
    # lfm_albumcover=result_info['track']['album']['image'][-1]['#text'].encode('UTF-8')  #-1=biggest,  -2=2nd biggest, and so on

    lfm_tags = []
    if 'tag' in result_tags['tags']:
        lfm_tags = [x['name'].encode('UTF-8') for x in result_tags['tags']['tag']]  # list of tags
    else:
        notfound_lfm_tags += 1
    # lfm_genres=[x for x in lfm_tags if x in genres] #search for tags with a genre
    lfm_genres = lfm_tags  # use all tags as genres
    # print(result_tags['tags'])

    published = ''  # year published, TODO

    for g in lfm_tags:
        genrecount[g] = genrecount.get(g, 0) + 1

    # similar titles in extra csv, nicht hier

    # print("album="+lfm_album)
    # print("albumcover="+lfm_albumcover)
    # print("tags="+str(lfm_tags))
    # print("genres="+str(lfm_genres))

    # artist_id = "c5c2ea1c-4bde-4f4d-bd0b-47b200bf99d6"
    # try:
    #    result = musicbrainzngs.get_artist_by_id(artist_id)
    # except WebServiceError as exc:
    #    print("Something went wrong with the request: %s" % exc)
    # else:
    #    artist = result["artist"]
    #    print("name:\t\t%s" % artist["name"])
    #    print("sort name:\t%s" % artist["sort-name"])

    print('%s: %s,%s,%s,%s,%s,%s,%s,%s,%s' % (
    counter, notfound_lfm_track, notfound_lfm_playcount, notfound_lfm_listeners, notfound_lfm_trackmbid,
    notfound_lfm_artistmbid, notfound_lfm_albummbid, notfound_lfm_album,
    notfound_lfm_albumcover, notfound_lfm_tags))

    csv_out.writerow((title, artist, lfm_album, songHash, length, published, lfm_trackmbid, lfm_artistmbid,
                      lfm_albummbid, lfm_playcount, lfm_listeners, lfm_albumcover, str(lfm_genres)))

with open('tags_out.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=genrecount.keys())

    writer.writeheader()
    writer.writerow(genrecount)

print(genrecount)
