from __future__ import unicode_literals
import musicbrainzngs
import sys
import time
import json
import csv
import urllib
import requests

artist_mbid = "ee224919-a673-473d-8368-777795c73fbf"
# artist_mbid = "ed4aa69e-e049-4ac4-90c3-869aee5decac"
artist = 'paddy and the rats'
album = 'hymns for bastards'
album_mbid = "9fd0681a-7f48-49b5-8855-b624e559d061"  # release-id
recording_mbid = "83a23515-5db5-45f9-8ec8-9be9f4003d00"
dict = {'artist': artist_mbid}
# artist ='ac/dc'
# album='Back in Black'
# artist = 'sean paul'
# album = 'she doesn\'t mind'

# country='GB'
# track='Hells+Bells'
# tag='rock'

datelist = []

# User-Agent string is needed for every request: App name, apps version number,
# contact-url or -email. This is an example:
musicbrainzngs.set_useragent(
    "python-musicbrainzngs-example",
    "0.1",
    "https://github.com/alastair/python-musicbrainzngs/",
)

musicbrainzngs.auth("reactivejukebox", "_hierspieltdiemusik4")


def iterate_over_file(csv_in):
    count = 0
    total = 0
    for rownum, row in enumerate(csv_in):
        if (len(row) <= 3) or (rownum == 0):  # line too short or first line
            continue
        artist = row[1]
        album = row[2]
        # print (search_tags(artist,album))
        print(search_releases(artist, album))
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
        genres = [x.strip().lower() for x in genres]  # remove whitespaces and linebreakes and make lower case
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
    if isinstance(first, str):
        f = first.lower()
    else:
        f = first.decode('UTF-8').lower()
    if isinstance(second, str):
        s = second.lower()
    else:
        s = second.decode('UTF-8').lower()

    f_in_s = s.find(f)
    s_in_f = f.find(s)

    if f_in_s > 0 or s_in_f > 0 or f == s:
        return True
    else:
        return False


# filter the search result for the release dates
def show_release_details(rel, artistname, albumname):
    data_artist = rel['artist-credit-phrase']
    data_album = rel['title']
    if compare_name(data_artist, artistname) and compare_name(data_album, albumname):
        if 'date' in rel:
            datelist.append(rel['date'])


# filter the date result list for the oldest release date
def show_first_release_date():
    datelist.sort()
    if len(datelist) != 0:
        erg = datelist[0]
        del datelist[:]
        return erg


def show_tags(rel):
    print(json.dumps(rel, indent=4))


# filter the search result for the oldest release date
def search_releases(result, artistname, albumname):
    if not result['release-list']:
        print("no release found")
        return
    for (idx, release) in enumerate(result['release-list']):
        show_release_details(release, artistname, albumname)
    return show_first_release_date()


# filter the search result for tags by artist (and not by recording/album!!!)
def search_tags(result, artistname):  # , albumname):
    genres = []
    if not result['release-list']:
        return []  # no list was found
    for (idx, release) in enumerate(result['release-list']):
        if not 'artist-credit-phrase' in release:
            print("No artist credit name given")
            # if not 'title' in release:
            #   continue
            # if not(release['title'].lower() == albumname.lower()):
            #   continue
        else:
            if (release['artist-credit-phrase'].lower() == artistname.lower()):
                if 'tag-list' in release:
                    for tag in release['tag-list']:
                        genres.append(tag['name'])
    return genres


# filter the search result for rating
def get_rank(result):
    if not 'rating' in result:
        # print("No rating given")
        return [None, None]
    else:
        rating_votes_count = result['rating']['votes-count']
        rating_value = result['rating']['value']
        return [rating_votes_count, rating_value]


def get_mb_result(artist_mbid):
    return json.loads(
        requests.get("http://musicbrainz.org/ws/2/artist/" + artist_mbid + "?inc=aliases+tags+ratings&fmt=json").text)


# filter the search result for tags
def get_tags(result):
    genres = []
    if not 'tags' in result:
        # print("No tags given")
        return genres  # return empty list
    else:
        for tag in result['tags']:
            genres.append(tag['name'])
    return genres


def get_search_result(artistname, albumname, lim):
    result = musicbrainzngs.search_releases(artist=artistname, release=albumname,
                                            limit=lim)
    return result


def get_recording_result(track_mbid):
    result = json.loads(
        requests.get("http://musicbrainz.org/ws/2/recording/" + track_mbid + "?inc=tags+ratings&fmt=json").text)
    return result


# delete doubles
def filter_genre_results(taglist):
    return sorted(set(taglist), key=taglist.index)


def test():
    # artist_id = "c5c2ea1c-4bde-4f4d-bd0b-47b200bf99d6"
    try:
        # result = musicbrainzngs.get_artist_by_id(artist_mbid, includes=['ratings'])
        result = musicbrainzngs.get_label_by_id(label_id, includes=['ratings'])
    except:
        print("Something went wrong with the request!")
    else:
        # artist = result["artist"]
        # print("name:\t\t%s" % artist["name"])
        # print("sort name:\t%s" % artist["sort-name"])
        show_tags(result)


def testrequest():
    result = json.loads(
        requests.get("http://musicbrainz.org/ws/2/recording/" + recording_mbid + "?inc=tags+ratings&fmt=json").text)
    show_tags(result)

# result = get_recording_result("805ac5ab-eafe-4520-8fb6-297eaf08f2d6")
# print (get_rank(result))
# result = get_search_result(artist,album,5)
# print (search_tags(result,artist,album))
# testrequest()
