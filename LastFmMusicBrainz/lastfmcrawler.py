#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

#Example Usage: python3 lastfmcrawler.py id3data.csv genres.csv

import csv
import json
import time
# import musicbrainzngs
import urllib
# import urllib2
# from urllib.request import urlopen
import urllib.parse
import operator
import musicbrainz_crawl_year_and_genre as mbcyag
import requests
import sys

# EXAMPLES:
artist = 'AC/DC'
track = 'Hells+Bells'


# similar artists to given artist
# result=json.load(urllib2.urlopen("http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist=cher&api_key=a8b40052edf6a8ce494429b0b3b10f91&format=json"))
# print([x['name'].encode('UTF-8') for x in result['similarartists']['artist'] ])

# tags to given track
# result=json.load(urllib2.urlopen("http://ws.audioscrobbler.com/2.0/?#method=track.getTags&api_key=a8b40052edf6a8ce494429b0b3b10f91&artist="+artist+"&track="+track+"&user=RJ&format=json"))
# print([x['name'].encode('UTF-8') for x in result['tags']['tag'] ])

# END EXAMPLES

not_inflate_tags=['rock & roll']

def normalizeTag(tagname):
    tagname = tagname.replace('-', ' ')  # rock-pop -> rock pop
    tagname = tagname.replace('\'', '')  # 90's -> 90s
    tagname = tagname.replace('+', ' ')  # dance+and+electronica -> dance and electronica
    tagname = tagname.replace('/', ' ')  # singer/songwriter -> singer songwriter
    tagname = tagname.replace('.', ' ')  # post.rock -> post rock
    tagname = tagname.replace('_', ' ')  # alternative_metal -> alternative metal
    return tagname


def inflate_tags(tags):
    tags_new = []
    for t in tags:  # 'alternative rock'
        if (t in not_inflate_tags):
            continue #skip not_inflate_tags tags
        if type(t) is not str:  # some tags can be of type 'byte' (for example Oasis - Wonderwall)
            t = t.decode('UTF-8')  # decode byte to string
        tt = t.split(' ')  # ['alternative','rock']
        if ('classic' in tt and len(tt)>1):
            tt.remove('classic') #remove 'classic', if it was part of a genre like 'classic rock'
        tt += [t]  # ['alternative', 'rock', 'alternative rock']
        tt = [x.rstrip() for x in tt]
        tags_new += tt

    return tags_new


def correct_tags(tags):  # correct common spelling mistakes
    tags_correct = []
    search_for = ['electonic', 'r&b', 'electro swing', 'synth pop', 'ragga', 'synthie pop', 'genre: deep house',
                  'rhythm and blues', 'hellektro', 'pbrnb', '1960s', '1970s', '1980s', '1990s', '00s', 'hiphop', 'triphop', 'edm', 'psy trance']
    replace_with = ['electronic', 'rnb', 'electroswing', 'synthpop', 'reggae', 'synthpop', 'deep house',
                    'rhythm & blues', 'aggrotech', 'alternative rnb', '60s', '70s', '80s', '90s', '2000s', 'hip hop', 'trip hop', 'electronic dance music', 'psytrance']
    for t in tags:
        for sfindex, sf in enumerate(search_for):
            t = t.replace(search_for[sfindex], replace_with[sfindex])
        tags_correct += [t]
    return tags_correct

infile = sys.argv[1]

genres=[]
if (len(sys.argv)>2):
    genrefile = sys.argv[2]

    # read genres
    with open(genrefile) as f:
        genres = f.readlines()
        genres = [x.strip().lower() for x in genres]  # remove whitespaces and linebreakes and make lower case

out = open("lastfmdata.csv", "w", encoding="utf-8", newline="")
csv_out = csv.writer(out, delimiter=',')

# csv_infile = open('beispiel.csv', "r")
# csv_in = csv.reader(csv_infile, delimiter=';')

csv_infile = open(infile, "r")
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
notfound_mb_tags = 0
notfound_mb_release = 0
notfound_track = 0
notfound_mb_rank = 0
notfound_mb_track_rank = 0

for rownum, row in enumerate(csv_in):
    #if rownum < 12260:
        #continue

    if len(row) <= 3:  # line too short
        continue

    if rownum == 0:  # header
        csv_out.writerow(('title', 'artist', 'album', 'songHash', 'length', 'published', 'trackmbid', 'artistmbid',
                          'albummbid', 'playcount', 'listeners', 'albumcover', 'genres', 'artistrating', 'trackrating'))
        continue  # next row

    title = row[0]
    artist = row[1]
    album = row[2]
    songHash = row[3]
    length = row[4]
    published=''
    if (len(row)>5):
        published = row[5] #not available for all
    print(str(rownum) + " t=" + str(round(time.time() - timestart)) + ": " + artist + " - " + title)

    apiParams = '&api_key=a8b40052edf6a8ce494429b0b3b10f91&artist=%s&track=%s&user=RJ&format=json' % (
        urllib.parse.quote(artist, safe=''), urllib.parse.quote(title, safe=''))
    infoURL = 'http://ws.audioscrobbler.com/2.0/?method=track.getInfo' + apiParams
    # result_info = json.loads( urllib.request.urlopen(infoURL).read()) #used before
    result_info = json.loads(requests.get(infoURL).text)

    tagURL = 'http://ws.audioscrobbler.com/2.0/?method=track.getTags' + apiParams
    result_tags = json.loads(requests.get(tagURL).text)

    counter += 1

    # initialize
    lfm_track = ''
    lfm_album = ''
    lfm_playcount = '0'
    lfm_listeners = '0'
    lfm_trackmbid = ''
    lfm_artistmbid = ''
    lfm_albummbid = ''
    lfm_albumcover = ''
    lfm_tags = []
    mb_another_tags = []
    mb_rating = ''
    mb_track_rating = ''

    if 'track' not in result_info:
        notfound_track += 1
    else:
        if 'name' in result_info['track']:
            lfm_track = result_info['track']['name']  # .encode('UTF-8')
        else:
            notfound_lfm_track += 1

        if 'playcount' in result_info['track']:
            lfm_playcount = result_info['track']['playcount']  # .encode('UTF-8')
        else:
            notfound_lfm_playcount += 1

        if 'listeners' in result_info['track']:
            lfm_listeners = result_info['track']['listeners']  # .encode('UTF-8')
        else:
            notfound_lfm_listeners += 1

        if 'mbid' in result_info['track']:
            lfm_trackmbid = result_info['track']['mbid']  # .encode('UTF-8')
        else:
            notfound_lfm_trackmbid += 1

        if 'artist' in result_info['track']:
            if 'mbid' in result_info['track']['artist']:
                lfm_artistmbid = result_info['track']['artist']['mbid']  # .encode('UTF-8')
            else:
                notfound_lfm_artistmbid += 1
        else:
            notfound_lfm_artistmbid += 1

        if 'album' in result_info['track']:
            if 'mbid' in result_info['track']['album']:
                lfm_albummbid = result_info['track']['album']['mbid']  # .encode('UTF-8')
            else:
                notfound_lfm_albummbid += 1
        else:
            notfound_lfm_albummbid += 1

        if 'album' in result_info['track']:
            if 'title' in result_info['track']['album']:
                lfm_album = result_info['track']['album']['title']  # .encode('UTF-8')
            else:
                notfound_lfm_album += 1
        else:
            notfound_lfm_album += 1

        if 'album' in result_info['track']:
            if 'image' in result_info['track']['album']:
                lfm_albumcover = result_info['track']['album']['image'][-1][
                    '#text']  # .encode('UTF-8')  #-1=biggest,  -2=2nd biggest, and so on
            else:
                notfound_lfm_albumcover += 1
        else:
            notfound_lfm_albumcover += 1

        if 'tags' in result_tags and 'tag' in result_tags['tags']:
            # lfm_tags = [x['name'].encode('UTF-8') for x in result_tags['tags']['tag']]  # list of tags
            lfm_tags = [x['name'] for x in result_tags['tags']['tag']]  # list of tags
        else:
            notfound_lfm_tags += 1
    tags = lfm_tags

    if lfm_artistmbid != '':
        mb_another_result = mbcyag.get_mb_result(
            lfm_artistmbid)  # search for infos about ratings and tags by the artist-id
        mb_another_tags = mbcyag.get_tags(
            mb_another_result)  # get tags from MusicBrianz by artist (and not by recording!!!)
        mb_rating = mbcyag.get_rank(mb_another_result)[1]  # get rating value
        if mb_rating is None:
            mb_rating = ''
            notfound_mb_rank += 1
    else:
        notfound_mb_rank += 1

    if lfm_trackmbid != '':
        mb_recording_result = mbcyag.get_recording_result(
            lfm_trackmbid)  # search for infos about ratings by the recording-id (track-id)
        mb_track_rating = mbcyag.get_rank(mb_recording_result)[1]  # get track rating value
        if mb_track_rating is None:
            mb_track_rating = ''
            notfound_mb_track_rank += 1

    mb_result = mbcyag.get_search_result(artist, album,
                                         50)  # search for infos about the album by the artist and crawl 50 results

    mb_tags = mbcyag.search_tags(mb_result, artist)  # get tags from MusicBrianz by artist (and not by recording!!!)
    if len(mb_tags) > 0:
        for x in mb_tags:
            tags.append(x)  # append musicbrainz tags to lastfm tags
    else:
        notfound_mb_tags += 1

    if len(mb_another_tags) > 0:  # Add more musicbrainz tags
        for x in mb_another_tags:
            tags.append(x)  # append musicbrainz tags to lastfm tags

    #tags = inflate_tags(tags)  # inflate tags (also fix utf8 tags), example: 'alternative rock' -> 'alternative rock','alternative','rock'
    #tags = [normalizeTag(t) for t in tags]  # normalize tags. for example replace '-' by ' '
    #tags = correct_tags(tags)  # correct typos

    #track_genres = [x for x in tags if x in genres]  # search for tags with a genre
    track_genres= [x for x in tags] #use all tags

    track_genres = mbcyag.filter_genre_results(track_genres)  # filter out duplicates

    if published=='':
        mb_published = mbcyag.search_releases(mb_result, artist, lfm_album)  # get oldest release date
        if mb_published == 0:
            mb_published = ''
            notfound_mb_release += 1
        published=mb_published #use musicbrainz published date if no published dated was previously given

    for g in tags:  # add tags from current track to genrecount dict
        genrecount[g] = genrecount.get(g, 0) + 1

    # print('%s: %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (
    #    counter, notfound_track, notfound_lfm_track, notfound_lfm_playcount, notfound_lfm_listeners,
    #    notfound_lfm_trackmbid,
    #    notfound_lfm_artistmbid, notfound_lfm_albummbid, notfound_lfm_album,
    #    notfound_lfm_albumcover, notfound_lfm_tags, notfound_mb_tags, notfound_mb_release, notfound_mb_rank))

    if len(album) == 0:  # no album in id3
        album = lfm_album  # use last.fm album (normally all mp3's have album names given)

    csv_out.writerow((title, artist, album, songHash, length, published, lfm_trackmbid, lfm_artistmbid,
                          lfm_albummbid, lfm_playcount, lfm_listeners, lfm_albumcover, str(track_genres), mb_rating,
                          mb_track_rating))

# write all tags (one tag only once)
genrecount_ordered_list = sorted(genrecount.items(), key=operator.itemgetter(1), reverse=True)
with open('tags_out.csv', 'w') as genrefile:
    # print(genrecount_ordered_list)
    for tag in genrecount_ordered_list:
        genrefile.write(str(tag[0])+ ',' + str(tag[1]) + '\n')

# print(genrecount_ordered_list)
print('stats')
print('%s: %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (
    counter, notfound_track, notfound_lfm_track, notfound_lfm_playcount, notfound_lfm_listeners, notfound_lfm_trackmbid,
    notfound_lfm_artistmbid, notfound_lfm_albummbid, notfound_lfm_album,
    notfound_lfm_albumcover, notfound_lfm_tags, notfound_mb_tags, notfound_mb_release, notfound_mb_rank,
    notfound_mb_track_rank))
